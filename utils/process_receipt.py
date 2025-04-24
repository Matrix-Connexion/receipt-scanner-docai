import os
import traceback
import streamlit as st
from google.cloud import documentai_v1beta3 as documentai


def get_entity_text(entity):
    """Safely extracts text from a Document AI entity."""
    if entity and entity.normalized_value and entity.normalized_value.text:
        return entity.normalized_value.text.strip()
    if entity and entity.mention_text:
        return entity.mention_text.strip()
    return None


def process_receipt(image_file, credentials, project_id, location, processor_id):
    """
    Processes a receipt image using Google Cloud Document AI Receipt Processor.
    """
    try:
        if not project_id or not location or not processor_id:
            st.error("Missing required Document AI configuration (project_id, location, processor_id).")
            return None

        client_options = {"api_endpoint": f"{location}-documentai.googleapis.com"}
        client = documentai.DocumentProcessorServiceClient(
            client_options=client_options,
            credentials=credentials
        )
        name = client.processor_path(project_id, location, processor_id)

        image_content = image_file.getvalue()
        file_extension = os.path.splitext(image_file.name)[1].lower()

        if file_extension in [".jpg", ".jpeg"]:
            mime_type = "image/jpeg"
        elif file_extension == ".png":
            mime_type = "image/png"
        elif file_extension in [".tif", ".tiff"]:
            mime_type = "image/tiff"
        elif file_extension == ".pdf":
            mime_type = "application/pdf"
        else:
            st.error(
                f"Unsupported file type: {file_extension}. Please upload JPG, PNG, TIFF, or PDF."
            )
            return None

        raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
        request = documentai.ProcessRequest(name=name, raw_document=raw_document)
        result = client.process_document(request=request)
        document = result.document

        if not document:
            st.error("Document AI did not return a valid document object.")
            return None
        if not document.text:
            st.warning("Document AI did not extract any text (OCR failed). Check image quality.")

        average_confidence = None
        if document.entities:
            confidences = [entity.confidence for entity in document.entities if hasattr(entity, "confidence")]
            if confidences:
                average_confidence = sum(confidences) / len(confidences)

        extracted_data = {
            "receipt_details": {},
            "line_items": [],
            "subtotal": None,
            "total_tax_amount": None,
            "total_discount_amount": None,
            "total_amount": None,
            "ocr_confidence": average_confidence,
        }

        entity_count = 0
        line_item_count = 0
        for entity in document.entities:
            entity_count += 1
            entity_type = entity.type_
            text_value = get_entity_text(entity)

            if entity_type == "line_item":
                line_item_count += 1
                item_data = {
                    "description": None,
                    "quantity": None,
                    "unit_price": None,
                    "total_price": None,
                }
                for prop in entity.properties:
                    prop_type = prop.type_
                    prop_text = get_entity_text(prop)
                    if prop_type == "description":
                        item_data["description"] = prop_text
                    elif prop_type == "quantity":
                        item_data["quantity"] = prop_text
                    elif prop_type in ["unit_price", "amount", "product_code"]:
                        item_data["unit_price"] = prop_text
                    elif prop_type in ["total_price", "price", "line_item_total"]:
                        item_data["total_price"] = prop_text
                extracted_data["line_items"].append(item_data)

            elif entity_type == "subtotal":
                extracted_data["subtotal"] = text_value
            elif entity_type == "total_tax_amount":
                extracted_data["total_tax_amount"] = text_value
            elif entity_type == "total_discount_amount":
                extracted_data["total_discount_amount"] = text_value
            elif entity_type == "total_amount":
                extracted_data["total_amount"] = text_value
            else:
                extracted_data["receipt_details"][entity_type] = text_value

        st.write(f"Processed {entity_count} entities, including {line_item_count} line items.")
        return extracted_data

    except Exception as e:
        st.error(f"Error processing document with Document AI: {e}")
        st.error("See console/terminal log for detailed traceback.")
        st.info("Check Document AI processor configuration and service account permissions.")
        print("--- ERROR TRACEBACK ---")
        print(traceback.format_exc())
        print("-----------------------")
        return None