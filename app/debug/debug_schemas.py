# debug_schema.py
import os
import sys

# Añade el directorio actual al path de Python para que encuentre 'app'
sys.path.append(os.getcwd())

try:
    print("--- Intentando importar AlertOut ---")
    from schemas.alert import AlertOut
    print("✅ AlertOut importado exitosamente.")
    
    print("\n--- Inspeccionando campos de AlertOut ---")
    for field_name, field_model in AlertOut.model_fields.items():
        print(f"Campo: '{field_name}', Tipo: {field_model.annotation}")
        
    print("\n--- Verificando la presencia de Session ---")
    # Intentamos buscar 'Session' en el texto del archivo de forma cruda
    with open("app/schemas/alert.py") as f:
        content = f.read()
        if "Session" in content:
            print("❌ ERROR GRAVE: La palabra 'Session' existe en app/schemas/alert.py")
        else:
            print("✅ El archivo app/schemas/alert.py no contiene la palabra 'Session'.")

except Exception as e:
    print(f"❌ Ocurrió un error al depurar: {e}")