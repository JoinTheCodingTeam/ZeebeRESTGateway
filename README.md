# Zeebe REST gateway
A stateless daemon for translating Zeebe gRPC calls to REST requests and vice versa.

## Usage
1. Install requirements
    ```
    pip install -r requirements.txt
    ```

2. Configure Zeebe connection and other options in `.env`. See `.env.example` for available options.

3. Build the web UI.
    ```
    npm run build --prefix=webui
    ```

4. Start the server
    ```
    uvicorn zeebe_rest_gateway.app:create_app --host 0.0.0.0 --port 8000 --log-config=logging.yaml
    ```


## Development
1. Configure `venv` with Python 3.8+ within the `.venv` directory.

2. Configure Zeebe connection and other options in `.env`. See `.env.example` for available options.
  
3. Install development requirements
    ```
    .venv/Scripts/pip install -r requirements.dev.txt
    ```

4. Update RPC specification file `zeebe_rest_gateway/spec/gateway.proto` with changes from [latest stable 
Zeebe version](https://github.com/camunda-cloud/zeebe/blob/clients/go%2Fv1.1.1/gateway-protocol/src/main/proto/gateway.proto).

5. Regenerate RPC implementation from spec
    ```
    make spec
    ``` 

6. Run tests
    ```
    make tests
    ```

7. Run linters (MyPy and PyLint):
    ```
    make init_linters
    make lint
    ```
   
8. Start web UI debug server:
    ```
    npm run dev --prefix=webui        
    ``` 
   
9. Start the debug server:
    ```
    make run_debug_server 
    ```

## Versioning
This service uses [Semantic Versioning](https://semver.org/), version is stored in `VERSION` file.
