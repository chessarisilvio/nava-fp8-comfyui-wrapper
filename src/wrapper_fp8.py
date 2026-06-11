import os
from typing import Dict, Any, Optional


class WrapperFP8:
    """
    Wrapper for initializing ComfyUI in FP8 mode.
    Handles FP8 configuration without running inference.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the FP8 wrapper.

        Args:
            config: Optional dictionary with FP8 configuration.
                   If not provided, loads from environment variables.
        """
        if config is not None:
            self.config = config
        else:
            self.config = self._load_from_env()

    def _load_from_env(self) -> Dict[str, Any]:
        """
        Load FP8 configuration from environment variables.

        Returns:
            Dictionary with FP8 settings.
        """
        config = {
            # Enable FP8 mode
            'fp8_enabled': os.environ.get('FP8_ENABLED', 'false').lower() == 'true',
            # FP8 format: 'e4m3' or 'e5m2'
            'fp8_format': os.environ.get('FP8_FORMAT', 'e4m3'),
            # Compute type for FP8 operations: 'bf16', 'fp16', 'fp32'
            'fp8_compute_type': os.environ.get('FP8_COMPUTE_TYPE', 'bf16'),
            # Whether to use FP8 for weights
            'fp8_weights': os.environ.get('FP8_WEIGHTS', 'true').lower() == 'true',
            # Whether to use FP8 for activations
            'fp8_activations': os.environ.get('FP8_ACTIVATIONS', 'true').lower() == 'true',
            # Additional ComfyUI-specific FP8 flags
            'comfyui_fp8_unet': os.environ.get('COMFYUI_FP8_UNET', 'true').lower() == 'true',
            'comfyui_fp8_vae': os.environ.get('COMFYUI_FP8_VAE', 'false').lower() == 'true',
            'comfyui_fp8_text_encoder': os.environ.get('COMFYUI_FP8_TEXT_ENCODER', 'false').lower() == 'true',
        }
        return config

    def get_fp8_config(self) -> Dict[str, Any]:
        """
        Get the current FP8 configuration.

        Returns:
            Dictionary containing FP8 settings.
        """
        return self.config.copy()

    def update_config(self, new_config: Dict[str, Any]) -> None:
        """
        Update the FP8 configuration.

        Args:
            new_config: Dictionary with configuration updates.
        """
        self.config.update(new_config)

    def is_fp8_enabled(self) -> bool:
        """
        Check if FP8 is enabled.

        Returns:
            True if FP8 is enabled, False otherwise.
        """
        return self.config.get('fp8_enabled', False)

    def to_env_dict(self) -> Dict[str, str]:
        """
        Convert configuration to environment variable dictionary.
        Useful for setting environment variables before launching ComfyUI.

        Returns:
            Dictionary with environment variable names and string values.
        """
        env_map = {
            'FP8_ENABLED': str(self.config.get('fp8_enabled', False)).lower(),
            'FP8_FORMAT': self.config.get('fp8_format', 'e4m3'),
            'FP8_COMPUTE_TYPE': self.config.get('fp8_compute_type', 'bf16'),
            'FP8_WEIGHTS': str(self.config.get('fp8_weights', True)).lower(),
            'FP8_ACTIVATIONS': str(self.config.get('fp8_activations', True)).lower(),
            'COMFYUI_FP8_UNET': str(self.config.get('comfyui_fp8_unet', True)).lower(),
            'COMFYUI_FP8_VAE': str(self.config.get('comfyui_fp8_vae', False)).lower(),
            'COMFYUI_FP8_TEXT_ENCODER': str(self.config.get('comfyui_fp8_text_encoder', False)).lower(),
        }
        return env_map


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Create wrapper from environment
    wrapper = WrapperFP8()
    print("FP8 Configuration:")
    for key, value in wrapper.get_fp8_config().items():
        print(f"  {key}: {value}")

    # Check if FP8 is enabled
    if wrapper.is_fp8_enabled():
        print("\nFP8 is ENABLED")
    else:
        print("\nFP8 is DISABLED")

    # Show environment variables for ComfyUI
    print("\nEnvironment variables for ComfyUI:")
    for key, value in wrapper.to_env_dict().items():
        print(f"  {key}={value}")