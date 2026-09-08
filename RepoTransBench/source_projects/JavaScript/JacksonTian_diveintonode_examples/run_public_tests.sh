#!/bin/bash
set -e

echo "Running public test suite (alternate data/ports/messages) with jest..."

jest 07/tls/tls_client_server.public.test.js
jest 07/tls/tls_server.public.test.js
jest 07/https/https_server_client.public.test.js
jest 07/http/http_client.public.test.js
jest 02/extensions.public.test.js
jest 05/delete.public.test.js
jest 05/parse.public.test.js

echo "All public tests executed."