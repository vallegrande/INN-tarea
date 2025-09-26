# Análisis de datos de salarios
# Dataset con info de empleados del sector tech
# Vamos a ver qué patrones encontramos aquí

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')  # para que no molesten los warnings

# configurar gráficos para que se vean bien
plt.style.use('default')
sns.set_palette("husl")

def main():
    # primero configuremos pandas para que se vea todo bien
    print("Configurando pandas...")
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1200) 
    pd.set_option("display.colheader_justify", "center")
    pd.set_option("display.max_rows", 50)
    
    # carguemos los datos a ver qué tenemos
    print("Cargando el CSV...")
    df = pd.read_csv("Salary_Data.csv")
    
    print("="*80)
    print("INFORMACIÓN BÁSICA DEL DATASET")
    print("="*80)
    print(f"Tenemos {df.shape[0]} filas y {df.shape[1]} columnas")
    print("\nLas columnas son:")
    print(df.columns.tolist())
    
    print("\nEchemos un vistazo a las primeras filas:")
    print(df.head().to_string(index=False))
    
    # ahora limpiemos un poco los datos
    print("\n" + "="*80)
    print("LIMPIEZA DE DATOS")
    print("="*80)
    
    print("Veamos la info general:")
    print(df.info())
    
    # revisemos qué datos faltan
    print("\nDatos faltantes por columna:")
    missing_values = df.isnull().sum()
    print(missing_values[missing_values > 0])
    
    # quitemos las filas completamente vacías si las hay
    df_clean = df.dropna(how='all')
    print(f"\nDespués de limpiar: {df_clean.shape[0]} filas")
    
    # veamos si hay salarios raros (muy bajos, probablemente errores)
    print("\nRevisando salarios sospechosos (menores a $10,000):")
    unusual_salaries = df_clean[df_clean['Salary'] < 10000]
    if not unusual_salaries.empty:
        print("Encontré estos salarios raros:")
        print(unusual_salaries[['Age', 'Job Title', 'Years of Experience', 'Salary']].to_string(index=False))
    else:
        print("No hay salarios sospechosos.")
    
    # ahora sí, vamos con las estadísticas
    print("\n" + "="*80)
    print("ESTADÍSTICAS GENERALES")
    print("="*80)
    print("Estadísticas descriptivas de todo:")
    print(df_clean.describe())
    
    print("\nEstadísticas específicas de salarios:")
    print(f"Promedio: ${df_clean['Salary'].mean():,.2f}")
    print(f"Mediana: ${df_clean['Salary'].median():,.2f}")
    print(f"Mínimo: ${df_clean['Salary'].min():,.2f}")
    print(f"Máximo: ${df_clean['Salary'].max():,.2f}")
    print(f"Desviación estándar: ${df_clean['Salary'].std():,.2f}")
    
    # veamos quiénes ganan más
    print("\n" + "="*80)
    print("TOP 15 SALARIOS MÁS ALTOS")
    print("="*80)
    top_salaries = df_clean.nlargest(15, "Salary")[["Age", "Gender", "Education Level", "Job Title", "Years of Experience", "Salary"]]
    print(top_salaries.to_string(index=False))
    
    # análisis por género (siempre interesante ver si hay diferencias)
    print("\n" + "="*80)
    print("ANÁLISIS POR GÉNERO")
    print("="*80)
    
    # cuántos hombres vs mujeres tenemos
    gender_counts = df_clean['Gender'].value_counts()
    print("Distribución por género:")
    print(gender_counts.to_string())
    
    # comparemos los salarios por género
    print("\nComparación de salarios por género:")
    gender_salary_stats = df_clean.groupby('Gender')['Salary'].agg([
        'count', 'mean', 'median', 'min', 'max', 'std'
    ]).round(2)
    gender_salary_stats.columns = ['Cantidad', 'Promedio', 'Mediana', 'Mínimo', 'Máximo', 'Desv.Std']
    print(gender_salary_stats.to_string())
    
    # calculemos la brecha salarial
    male_avg = df_clean[df_clean['Gender'] == 'Male']['Salary'].mean()
    female_avg = df_clean[df_clean['Gender'] == 'Female']['Salary'].mean()
    gender_gap = male_avg - female_avg
    gender_gap_pct = (gender_gap / female_avg) * 100
    
    print(f"\nBRECHA SALARIAL:")
    print(f"Diferencia: ${gender_gap:,.2f} ({gender_gap_pct:.2f}% más para hombres)")
    
    # ahora veamos cómo afecta la educación
    print("\n" + "="*80)
    print("ANÁLISIS POR EDUCACIÓN")
    print("="*80)
    
    # qué nivel educativo es más común
    education_counts = df_clean['Education Level'].value_counts()
    print("Niveles educativos en el dataset:")
    print(education_counts.to_string())
    
    # y cómo se comparan los salarios
    print("\nSalarios por nivel educativo (ordenados por promedio):")
    education_salary_stats = df_clean.groupby('Education Level')['Salary'].agg([
        'count', 'mean', 'median', 'min', 'max'
    ]).round(2).sort_values('mean', ascending=False)
    education_salary_stats.columns = ['Cantidad', 'Promedio', 'Mediana', 'Mínimo', 'Máximo']
    print(education_salary_stats.to_string())
    
    # cuáles son los trabajos mejor pagados
    print("\n" + "="*80)
    print("TOP 15 PUESTOS MEJOR PAGADOS")
    print("="*80)
    top_jobs = df_clean.groupby('Job Title')['Salary'].agg([
        'count', 'mean', 'median'
    ]).round(2).sort_values('mean', ascending=False).head(15)
    top_jobs.columns = ['Cantidad', 'Salario_Promedio', 'Salario_Mediano']
    print(top_jobs.to_string())
    
    # y cuáles son los más comunes
    print("\n" + "="*80)
    print("PUESTOS MÁS FRECUENTES")
    print("="*80)
    job_counts = df_clean['Job Title'].value_counts().head(15)
    print(job_counts.to_string())
    
    # la experiencia debe ser clave, veamos
    print("\n" + "="*80)
    print("ANÁLISIS POR EXPERIENCIA")
    print("="*80)
    
    # voy a crear rangos para que sea más fácil de analizar
    df_clean['Experience_Range'] = pd.cut(df_clean['Years of Experience'], 
                                        bins=[0, 2, 5, 10, 15, 100], 
                                        labels=['0-2 años', '3-5 años', '6-10 años', '11-15 años', '16+ años'])
    
    experience_salary_stats = df_clean.groupby('Experience_Range')['Salary'].agg([
        'count', 'mean', 'median'
    ]).round(2)
    experience_salary_stats.columns = ['Cantidad', 'Salario_Promedio', 'Salario_Mediano']
    print(experience_salary_stats.to_string())
    
    print(f"\nDatos de experiencia:")
    print(f"Promedio: {df_clean['Years of Experience'].mean():.2f} años")
    print(f"Rango: {df_clean['Years of Experience'].min()} - {df_clean['Years of Experience'].max()} años")
    
    # también veamos por edad
    print("\n" + "="*80)
    print("ANÁLISIS POR EDAD")
    print("="*80)
    
    # rangos de edad para comparar mejor
    df_clean['Age_Range'] = pd.cut(df_clean['Age'], 
                                 bins=[20, 25, 30, 35, 40, 45, 50, 100], 
                                 labels=['21-25', '26-30', '31-35', '36-40', '41-45', '46-50', '51+'])
    
    age_salary_stats = df_clean.groupby('Age_Range')['Salary'].agg([
        'count', 'mean', 'median'
    ]).round(2)
    age_salary_stats.columns = ['Cantidad', 'Salario_Promedio', 'Salario_Mediano']
    print(age_salary_stats.to_string())
    
    print(f"\nDatos de edad:")
    print(f"Promedio: {df_clean['Age'].mean():.2f} años")
    print(f"Rango: {df_clean['Age'].min()} - {df_clean['Age'].max()} años")
    
    # esto está interesante: género + educación
    print("\n" + "="*80)
    print("CRUCE: GÉNERO Y EDUCACIÓN")
    print("="*80)
    
    # tabla cruzada para ver patrones
    gender_education_salary = df_clean.pivot_table(
        values='Salary', 
        index='Education Level', 
        columns='Gender', 
        aggfunc='mean'
    ).round(2)
    
    print("Salarios promedio por género y educación:")
    print(gender_education_salary.to_string())
    
    # y cuántos hay en cada categoría
    gender_education_count = df_clean.pivot_table(
        values='Salary', 
        index='Education Level', 
        columns='Gender', 
        aggfunc='count'
    )
    
    print("\nCantidad de personas por género y educación:")
    print(gender_education_count.to_string())
    
    # veamos las correlaciones entre las variables numéricas
    print("\n" + "="*80)
    print("CORRELACIONES")
    print("="*80)
    
    # solo las columnas numéricas
    numeric_cols = ['Age', 'Years of Experience', 'Salary']
    correlation_matrix = df_clean[numeric_cols].corr().round(3)
    print("Matriz de correlación:")
    print(correlation_matrix.to_string())
    
    print(f"\nPuntos interesantes:")
    print(f"• Edad vs Salario: {correlation_matrix.loc['Age', 'Salary']:.3f}")
    print(f"• Experiencia vs Salario: {correlation_matrix.loc['Years of Experience', 'Salary']:.3f}")
    print(f"• Edad vs Experiencia: {correlation_matrix.loc['Age', 'Years of Experience']:.3f}")
    print("(Más cerca de 1 = más correlacionados)")
    
    # resumen de todo lo que encontramos
    print("\n" + "="*80)
    print("RESUMEN DE HALLAZGOS")
    print("="*80)
    
    print(f"Datos generales:")
    print(f"• Analizamos {df_clean.shape[0]:,} registros")
    print(f"• Salario promedio: ${df_clean['Salary'].mean():,.2f}")
    print(f"• Rango: ${df_clean['Salary'].min():,.0f} - ${df_clean['Salary'].max():,.0f}")
    
    print(f"\nPor género:")
    male_pct = (df_clean['Gender'].value_counts()['Male'] / len(df_clean)) * 100
    female_pct = (df_clean['Gender'].value_counts()['Female'] / len(df_clean)) * 100
    print(f"• {male_pct:.1f}% hombres, {female_pct:.1f}% mujeres")
    print(f"• Los hombres ganan {gender_gap_pct:.2f}% más en promedio")
    
    print(f"\nPor educación:")
    for edu in df_clean['Education Level'].value_counts().index:
        count = df_clean['Education Level'].value_counts()[edu]
        pct = (count / len(df_clean)) * 100
        avg_salary = df_clean[df_clean['Education Level'] == edu]['Salary'].mean()
        print(f"• {edu}: {pct:.1f}% (${avg_salary:,.0f} promedio)")
    
    print(f"\nOtros datos:")
    avg_exp = df_clean['Years of Experience'].mean()
    print(f"• Experiencia promedio: {avg_exp:.1f} años")
    print(f"• La experiencia correlaciona {correlation_matrix.loc['Years of Experience', 'Salary']:.3f} con el salario")
    
    # el puesto que más paga
    best_paid_job = df_clean.groupby('Job Title')['Salary'].mean().idxmax()
    best_paid_salary = df_clean.groupby('Job Title')['Salary'].mean().max()
    print(f"• Puesto mejor pagado: {best_paid_job} (${best_paid_salary:,.0f})")
    
    print("\n" + "="*80)
    print("Listo! El análisis está completo.")
    print("="*80)
    
    return df_clean

def generate_visualizations(df_clean):
    # función para hacer algunos gráficos básicos
    print("\nHaciendo unos gráficos...")
    
    plt.rcParams['figure.figsize'] = (12, 8)
    
    # histograma de salarios
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.hist(df_clean['Salary'], bins=50, edgecolor='black', alpha=0.7)
    plt.title('Distribución de Salarios')
    plt.xlabel('Salario ($)')
    plt.ylabel('Frecuencia')
    
    # boxplot por género
    plt.subplot(1, 2, 2)
    df_clean.boxplot(column='Salary', by='Gender', ax=plt.gca())
    plt.title('Salarios por Género')
    plt.suptitle('')  # quitar el título feo que pone automático
    
    plt.tight_layout()
    plt.savefig('salary_analysis_plots.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Gráficos guardados como 'salary_analysis_plots.png'")

if __name__ == "__main__":
    print("Iniciando análisis de datos de salarios...")
    print("="*80)
    
    try:
        # ejecutar el análisis principal
        df_clean = main()
        
        # preguntar si quiere gráficos
        generate_viz = input("\n¿Quieres que haga algunos gráficos? (y/n): ").lower().strip()
        if generate_viz in ['y', 'yes', 'sí', 'si']:
            generate_visualizations(df_clean)
        
        print("\nTodo listo!")
        
    except FileNotFoundError:
        print("Error: No encuentro el archivo 'Salary_Data.csv'")
        print("Asegúrate de que esté en la misma carpeta que este script.")
    except Exception as e:
        print(f"Algo salió mal: {e}")
        print("Revisa los datos y vuelve a intentar.")
