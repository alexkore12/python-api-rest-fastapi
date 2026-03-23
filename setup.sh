#!/bin/bash
# python-api-rest-fastapi Setup Script
# Instala dependencias y configura el entorno Python

set -euo pipefail

echo "🐍 python-api-rest-fastapi - Configuración"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

check_python() {
    if command -v python3 &> /dev/null; then
        echo -e "${GREEN}✓ Python3 encontrado: $(python3 --version)${NC}"
    else
        echo -e "${RED}✗ Python3 no encontrado${NC}"
        exit 1
    fi
}

check_venv() {
    if [ -d "venv" ]; then
        echo -e "${GREEN}✓ Entorno virtual existente${NC}"
    else
        echo -e "${YELLOW}⚠ Creando entorno virtual...${NC}"
        python3 -m venv venv
        echo -e "${GREEN}✓ Entorno virtual creado${NC}"
    fi
}

install_deps() {
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Dependencias instaladas${NC}"
}

setup_env() {
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
            echo -e "${GREEN}✓ Archivo .env creado${NC}"
        fi
    else
        echo -e "${GREEN}✓ Archivo .env ya existe${NC}"
    fi
}

main() {
    echo "Iniciando configuración..."
    check_python
    check_venv
    install_deps
    setup_env
    
    echo ""
    echo "======================================"
    echo -e "${GREEN}✓ Configuración completada!${NC}"
    echo "======================================"
    echo ""
    echo "Para iniciar el API:"
    echo "  source venv/bin/activate"
    echo "  uvicorn main:app --reload"
    echo ""
    echo "Docker:"
    echo "  docker build -t python-api ."
    echo "  docker run -d -p 8000:8000 python-api"
    echo ""
    echo "Documentación:"
    echo "  http://localhost:8000/docs"
}

main "$@"
