import argparse

def main():
    parser = argparse.ArgumentParser(description='Detector de Gluten en Comida')
    parser.add_argument('--port', type=int, default=5000, help='Puerto para el servidor Flask')
    args = parser.parse_args()

    # Aquí puedes iniciar tu servidor Flask con el puerto especificado
    from app import app
    app.run(port=args.port)

if __name__ == '__main__':
    main()
