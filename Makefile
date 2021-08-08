SCRIPTS_DIR=.venv/Scripts
PYTHON=${SCRIPTS_DIR}/python
ZEEBE_GATEWAY_SPEC_DIR=./zeebe_rest_gateway/spec

.PHONY: lint init_linters tests spec run_debug_server

lint:
	${SCRIPTS_DIR}/mypy.exe zeebe_rest_gateway
	${SCRIPTS_DIR}/pylint zeebe_rest_gateway

init_linters:
	${SCRIPTS_DIR}/mypy.exe --install-types --non-interactive

tests:
	${PYTHON} -m pytest

spec:
	${PYTHON} -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. ${ZEEBE_GATEWAY_SPEC_DIR}/gateway.proto

run_debug_server:
	${PYTHON} -m uvicorn zeebe_rest_gateway.app:create_app --factory --log-config=logging.yaml \
														   --reload --reload-dir=zeebe_rest_gateway
