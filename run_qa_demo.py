#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐾 PET GUARDIAN — GUARDIAN AI | RUNNER OFICIAL DE QA SPRINT 4
Challenge CLYVO VET 2026 — FIAP (2TDSPG) | IoT, IoB & IA Generativa

Uso direto no terminal:
    python run_qa_demo.py
    python run_qa_demo.py --delay 0.5
    python run_qa_demo.py --mode api --url https://deploy-guardianai-render.onrender.com
"""
import os
import sys
import subprocess

# Garante saída UTF-8 no terminal Windows (emojis e acentuação)
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

def main():
    # Localiza o diretório do script atual
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Procura test_sprint4_scenarios.py nos caminhos possíveis
    candidate_paths = [
        os.path.join(base_dir, "deploy_guardianai_render", "test_sprint4_scenarios.py"),
        os.path.join(base_dir, "test_sprint4_scenarios.py"),
        os.path.join(base_dir, "..", "deploy_guardianai_render", "test_sprint4_scenarios.py"),
    ]
    
    target_script = None
    for p in candidate_paths:
        if os.path.isfile(p):
            target_script = os.path.abspath(p)
            break
            
    if not target_script:
        print("[ERRO] Não foi possível localizar o arquivo 'test_sprint4_scenarios.py'.")
        print(f"Diretório base verificado: {base_dir}")
        sys.exit(1)
        
    target_cwd = os.path.dirname(target_script)

    # Argumentos padrão para a gravação (mode local com delay de 0.8s para leitura natural)
    user_args = sys.argv[1:]
    if not any(arg.startswith("--mode") for arg in user_args):
        user_args.extend(["--mode", "local"])
    if not any(arg.startswith("--delay") for arg in user_args):
        user_args.extend(["--delay", "0.8"])

    cmd = [sys.executable, target_script] + user_args
    
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    try:
        result = subprocess.run(cmd, cwd=target_cwd, env=env)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n\nExecução interrompida pelo usuário.")
        sys.exit(0)

if __name__ == "__main__":
    main()
