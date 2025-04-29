import pandas as pd
import io

def generate_export(format, results):
    buffer = io.BytesIO()

    if format == "xlsx":
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            for table, rows in results.items():
                df = pd.DataFrame(rows)
                df.to_excel(writer, sheet_name=table[:31], index=False)
    else:  # CSV
        table, rows = list(results.items())[0]
        df = pd.DataFrame(rows)
        df.to_csv(buffer, index=False)

    buffer.seek(0)
    filename = f"export_result.{format}"
    return buffer, filename
