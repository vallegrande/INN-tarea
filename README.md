# Análisis de Datos de Salarios

Un análisis exploratorio del mercado salarial en el sector tecnológico basado en un dataset de más de 6,700 registros de empleados.

## Descripción

Este proyecto analiza patrones salariales en la industria tech, examinando factores como género, educación, experiencia y tipo de puesto. Los datos revelan insights interesantes sobre brechas salariales y tendencias del mercado laboral.

## Dataset

- **Registros**: 6,704 empleados
- **Variables**: Edad, género, educación, puesto, experiencia, salario
- **Rango salarial**: $350 - $250,000
- **Promedio**: $115,327

## Principales Hallazgos

### Por Género
- 54.8% hombres, 45.0% mujeres
- Brecha salarial del 12.51% a favor de los hombres
- Diferencia promedio de $13,501

### Por Educación
- **PhD**: $165,685 promedio
- **Master's**: $157,604 promedio  
- **Bachelor's**: $85,175 promedio
- **High School**: $36,707 promedio

### Por Experiencia
- Correlación fuerte con salario (0.809)
- 0-2 años: $53,012
- 16+ años: $184,200

### Puestos Mejor Pagados
1. CEO - $250,000
2. Chief Technology Officer - $250,000
3. Chief Data Officer - $220,000
4. Director of Data Science - $204,561

## Requisitos

```bash
pip install pandas matplotlib seaborn numpy
```

## Uso

```bash
python salary_analysis.py
```

El script genera:
- Análisis estadístico completo
- Comparaciones por demografía
- Correlaciones entre variables
- Visualizaciones opcionales

## Estructura del Proyecto

```
├── salary_analysis.py      # Script principal de análisis
├── Salary_Data.csv        # Dataset original
├── salary_analysis_plots.png  # Gráficos generados
└── README.md             # Este archivo
```

## Resultados

El análisis identifica patrones claros en la compensación:

- La experiencia es el factor más predictivo del salario
- Existe una brecha de género significativa en todos los niveles educativos
- Los puestos de liderazgo (C-level, Directors) dominan los salarios más altos
- El nivel educativo tiene un impacto directo en la compensación

## Metodología

1. **Limpieza de datos**: Identificación y manejo de valores atípicos
2. **Análisis exploratorio**: Estadísticas descriptivas por segmento
3. **Análisis de correlación**: Relaciones entre variables numéricas
4. **Segmentación**: Comparaciones por demografía y rol
5. **Visualización**: Gráficos para insights clave

## Notas Técnicas

- Se detectaron 4 salarios anómalamente bajos (posibles errores de entrada)
- La correlación edad-experiencia es muy alta (0.938)
- Los datos incluyen una pequeña categoría "Other" para género (14 registros)

---

*Análisis realizado con Python y pandas para explorar tendencias del mercado laboral tech.*