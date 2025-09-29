import os
import subprocess
import sys

def run_command(cmd, desc):
    print(f"\n--- {desc} ---")
    try:
        subprocess.run(cmd, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de '{desc}': {e}")

def main():
    print("Diagnostic du projet Python\n")

    # 1. Vérification de l'environnement Python
    print(f"Version de Python: {sys.version}")

    # 2. Analyse statique avec pylint
    run_command("pip install pylint", "Installation de pylint")
    run_command("pylint .", "Analyse statique du code (pylint)")

    # 3. Installation des dépendances
    if os.path.exists("requirements.txt"):
        run_command("pip install -r requirements.txt", "Installation des dépendances")

    # 4. Exécution des tests unitaires
    run_command("python -m unittest discover", "Exécution des tests unitaires")

if __name__ == "__main__":
    main()