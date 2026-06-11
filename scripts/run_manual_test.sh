#!/bin/bash
# Manual test script for NAVA FP8 ComfyUI Wrapper
# Run this when GPUs are free to test FP8 configuration

set -euo pipefail

echo "=== NAVA FP8 ComfyUI Wrapper - Manual Test ==="

# Change to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

# Load virtual environment if exists
if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Test 1: Import wrapper and check default config
echo -e "\n[Test 1] Testing wrapper import and default configuration..."
python3 -c "
from src.wrapper_fp8 import WrapperFP8
wrapper = WrapperFP8()
print('FP8 enabled:', wrapper.is_fp8_enabled())
print('Config:', wrapper.get_fp8_config())
"

# Test 2: Test with custom config
echo -e "\n[Test 2] Testing wrapper with custom configuration..."
python3 -c "
from src.wrapper_fp8 import WrapperFP8
config = {
    'fp8_enabled': True,
    'fp8_format': 'e5m2',
    'fp8_compute_type': 'fp16',
    'fp8_weights': False,
    'fp8_activations': True,
    'comfyui_fp8_unet': True,
    'comfyui_fp8_vae': True,
    'comfyui_fp8_text_encoder': True,
}
wrapper = WrapperFP8(config)
print('FP8 enabled:', wrapper.is_fp8_enabled())
print('Format:', wrapper.get_fp8_config()['fp8_format'])
print('Compute type:', wrapper.get_fp8_config()['fp8_compute_type'])
env_dict = wrapper.to_env_dict()
print('Env vars sample:', {k: env_dict[k] for k in list(env_dict.keys())[:3]})
"

# Test 3: Test environment variable loading
echo -e "\n[Test 3] Testing environment variable configuration..."
FP8_ENABLED=true FP8_FORMAT=e5m2 FP8_COMPUTE_TYPE=fp32 FP8_WEIGHTS=false python3 -c "
from src.wrapper_fp8 import WrapperFP8
wrapper = WrapperFP8()
print('FP8 enabled from env:', wrapper.is_fp8_enabled())
print('Format from env:', wrapper.get_fp8_config()['fp8_format'])
print('Compute type from env:', wrapper.get_fp8_config()['fp8_compute_type'])
print('Weights from env:', wrapper.get_fp8_config()['fp8_weights'])
"

# Test 4: Show to_env_dict output
echo -e "\n[Test 4] Testing environment variable export..."
python3 -c "
from src.wrapper_fp8 import WrapperFP8
wrapper = WrapperFP8({'fp8_enabled': True})
env_vars = wrapper.to_env_dict()
for k, v in env_vars.items():
    print(f'export {k}={v}')
"

echo -e "\n=== All tests completed successfully ==="
echo "Next steps:"
echo "1. Set environment variables as shown above"
echo "2. Launch ComfyUI: python3 -m comfyui.execution --listen --port 8188"
echo "3. Verify FP8 usage in ComfyUI logs or via monitoring"