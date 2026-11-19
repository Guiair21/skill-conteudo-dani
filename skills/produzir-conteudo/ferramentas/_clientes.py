# -*- coding: utf-8 -*-
"""Resolve a pasta de config de cada cliente do motor de conteúdo.

Ordem de busca:
1. Variável de ambiente MOTOR_CONFIG_DIR (pasta que contém uma subpasta por cliente).
2. A pasta config/ na raiz do repositório (dois níveis acima de skills/produzir-conteudo).

Nada fora do repositório é lido se a variável não estiver definida.
"""
import os

_AQUI = os.path.dirname(os.path.abspath(__file__))
# ferramentas -> produzir-conteudo -> skills -> raiz do repositório
_RAIZ = os.path.abspath(os.path.join(_AQUI, '..', '..', '..'))


def pasta_base():
    return os.environ.get('MOTOR_CONFIG_DIR') or os.path.join(_RAIZ, 'config')


def pasta_cliente(nome):
    return os.path.join(pasta_base(), nome)


def listar_clientes():
    """Subpastas da pasta de config, em ordem alfabética."""
    base = pasta_base()
    if not os.path.isdir(base):
        return []
    return sorted(d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d)))
