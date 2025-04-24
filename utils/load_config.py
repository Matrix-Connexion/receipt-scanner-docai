import yaml
import streamlit as st


def load_docai_config(config_path="config.yaml"):
    """
    Load the configuration file and return Document AI parameters
    (excluding the key path, which is handled by the environment variable).

    Args:
        config_path (str): The path to the YAML configuration file.

    Returns:
        dict: A dictionary containing config values, or None if loading fails.
              Keys: 'project_id', 'location', 'processor_id'
    """
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            required_keys = [
                "google_cloud_project",
                "docai_location",
                "docai_processor_id",
            ]
            if not all(key in config for key in required_keys):
                st.error(
                    f"Config file '{config_path}' is missing one or more required keys: {required_keys}"
                )
                return None

            return {
                "project_id": config.get("google_cloud_project"),
                "location": config.get("docai_location"),
                "processor_id": config.get("docai_processor_id"),
            }
    except FileNotFoundError:
        return None
    except yaml.YAMLError as e:
        st.error(f"Error parsing configuration file '{config_path}': {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while loading config: {e}")
        return None
