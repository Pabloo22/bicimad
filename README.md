# Análisis predictivo de la demanda en estaciones BiciMad

## Introducción

Con este proyecto se busca comprobar la hipótesis de que estaciones de BiciMad cercanas tendrán comportamientos de demanda similares. 

Para ello, se utilizarán datos públicamente disponibles en:
- [GENERALES BICIMAD](https://opendata.emtmadrid.es/Datos-estaticos/Datos-generales-(1))
- [Especificaciones de los datos](https://opendata.emtmadrid.es/Documentos/Servicios-y-estructuras-Bicimad-V1-1.aspx)

En concreto, los datos de los ficheros json del tipo “Situación estaciones bicimad por día y hora de {mes}de 2022”.

## Motivación

Con los resultados obtenidos se pretende **entender mejor el comportamiento de los usuarios**. Por ejemplo, conocer si dicha relación existe, podría ser de utilidad para crear mejores modelos predictivos de la demanda, que a su vez permitan **mejorar la disponibilidad de bicicletas en las estaciones donde se predigan picos de demanda**.

## Aplicación

La forma en la que comprobaremos la hipótesis planteada será evaluando empíricamente si añadir datos de relaciones cercanas mejora o no las predicciones conseguidas. Para ello, se utilizará un modelo del tipo SARIMAX.

La distancia geográfica entre estaciones utilizando los datos de longitud y latitud. Con estos datos podremos seleccionar las “k” estaciones más cercanas o filtrar las estaciones por un threshold de distancia. Estas se utilizarán para mejorar la predicción original, y comprobar así también la eficacia para distintos valores de “k” o del threshold.
