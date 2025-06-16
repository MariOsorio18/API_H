from flask import Flask, render_template, request, jsonify
import networkx as nx
import math
import os

app = Flask(__name__)

casetas = [
    {"nombre": "Caseta Cuernavaca-Acapulco", "lat": 18.9261, "lon": -99.3197, "costo": 640.00},
    {"nombre": "Caseta Cuernavaca-Central de Abastos", "lat": 18.9261, "lon": -99.3197, "costo": 10.00},
    {"nombre": "Caseta Cuernavaca-Aeropuerto", "lat": 18.80247, "lon": -99.22045, "costo": 15.00},
    {"nombre": "Caseta Aeropuerto-Cuernavaca", "lat": 18.80247, "lon": -99.22045, "costo": 15.00},
    {"nombre": "Caseta Cuernavaca-Xochitepec", "lat": 18.7812, "lon": -99.3181, "costo": 32.00},
    {"nombre": "Caseta Xochitepec-Alpuyeca", "lat": 18.7403, "lon": -99.2604, "costo": 9.00},
    {"nombre": "Caseta Cuernavaca-Puente de Ixtla", "lat": 18.9261, "lon": -99.3197, "costo": 95.00},
    {"nombre": "Caseta Cuernavaca-Alpuyeca", "lat": 18.9261, "lon": -99.3197, "costo": 65.00},
    {"nombre": "Caseta Alpuyeca-Puente de Ixtla", "lat": 18.7403, "lon": -99.2604, "costo": 31.00},
    {"nombre": "Caseta Puente de Ixtla-Chilpancingo", "lat": 18.6147, "lon": -99.3181, "costo": 200.00},
    {"nombre": "Caseta Puente de Ixtla-Paso Morelos", "lat": 18.6147, "lon": -99.3181, "costo": 76.00},
    {"nombre": "Caseta Paso Morelos-Chilpancingo", "lat": 18.6147, "lon": -99.3181, "costo": 120.00},
    {"nombre": "Caseta Chilpancingo-Tierra Colorada", "lat": 17.55, "lon": -99.5, "costo": 182.00},
    {"nombre": "Caseta Tierra Colorada-Acapulco", "lat": 17.55, "lon": -99.5, "costo": 163.00},
    {"nombre": "Caseta Córdoba-Veracruz", "lat": 18.9, "lon": -96.95, "costo": 270.00},
    {"nombre": "Caseta Córdoba-La Tinaja", "lat": 18.9, "lon": -96.95, "costo": 140.00},
    {"nombre": "Caseta Córdoba-Cuitláhuac", "lat": 18.9, "lon": -96.95, "costo": 49.00},
    {"nombre": "Caseta Cuitláhuac-La Tinaja", "lat": 18.9, "lon": -96.95, "costo": 96.00},
    {"nombre": "Caseta La Tinaja-Veracruz", "lat": 18.9, "lon": -96.95, "costo": 130.00},
    {"nombre": "Caseta La Tinaja-Paso del Toro", "lat": 18.9, "lon": -96.95, "costo": 106.00},
    {"nombre": "Caseta Paso del Toro-Veracruz", "lat": 18.9, "lon": -96.95, "costo": 20.00},
    {"nombre": "Caseta La Tinaja-Cosoleacaque", "lat": 18.9, "lon": -96.95, "costo": 535.00},
    {"nombre": "Caseta La Tinaja-Isla", "lat": 18.9, "lon": -96.95, "costo": 277.00},
    {"nombre": "Caseta La Tinaja-Cosamaloapan", "lat": 18.9, "lon": -96.95, "costo": 229.00},
    {"nombre": "Caseta Cosamaloapan-Isla", "lat": 18.9, "lon": -96.95, "costo": 47.00},
    {"nombre": "Caseta Isla-Cosoleacaque", "lat": 18.9, "lon": -96.95, "costo": 258.00},
    {"nombre": "Caseta Isla-Acayucan", "lat": 18.9, "lon": -96.95, "costo": 167.00},
    {"nombre": "Caseta Acayucan-Cosoleacaque", "lat": 18.9, "lon": -96.95, "costo": 96.00},
    {"nombre": "Caseta Libramiento Noreste Querétaro", "lat": 20.5870, "lon": -100.3890, "costo": 62.00},
    {"nombre": "LAS CHOAPAS-OCOZOCOAUTLA", "lat": 17.5426, "lon": -94.4232, "costo": 65},
    {"nombre": "LAS CHOAPAS (D) ENT. LAS CHOAPAS - ENT. NUEVO SACRIFICIO", "lat": 17.5370, "lon": -94.4310, "costo": 30},
    {"nombre": "LAS CHOAPAS (I1) ENT. LAS CHOAPAS - ENT. LAS CHOAPAS II", "lat": 17.5350, "lon": -94.4200, "costo": 20},
    {"nombre": "LAS CHOAPAS (I2) ENT.LAS CHOAPAS II - ENT.NUEVO SACRIFICIO", "lat": 17.5300, "lon": -94.4150, "costo": 25},
    {"nombre": "MALPASITO (D) ENT. NUEVO SACRIFICIO - ENT. RAUDALES", "lat": 17.5200, "lon": -94.4000, "costo": 40},
    {"nombre": "MALPASITO (I1) ENT. NUEVO SACRIFICIO - ENT. MALPASITO", "lat": 17.5150, "lon": -94.3950, "costo": 18},
    {"nombre": "MALPASITO (I2) ENT. MALPASITO - ENT. RAUDALES", "lat": 17.5100, "lon": -94.3900, "costo": 22},
    {"nombre": "OCOZOCOAUTLA (OCUILAPA) (D) ENT. RAUDALES - ENT. OCOZOCOAUTLA", "lat": 17.4750, "lon": -92.8900, "costo": 50},
    {"nombre": "MEXICO-QUERETARO", "lat": 19.4326, "lon": -99.1332, "costo": 150},
    {"nombre": "TEPOTZOTLAN MEXICO TEPEJI", "lat": 19.7854, "lon": -99.2815, "costo": 70},
    {"nombre": "JOROBAS JOROBAS-TEPEJI", "lat": 19.7660, "lon": -99.3400, "costo": 55},
    {"nombre": "JOROBAS (CEM) JOROBAS-TEPEJI", "lat": 19.7660, "lon": -99.3400, "costo": 55},
    {"nombre": "PALMILLAS TEPEJI-PALMILLAS", "lat": 19.7110, "lon": -99.3150, "costo": 45},
    {"nombre": "PALMILLAS BIS TEPEJI-PALMILLAS", "lat": 19.7110, "lon": -99.3150, "costo": 45},
    {"nombre": "POLOTITLAN TEPEJI-POLOTITLAN", "lat": 19.6750, "lon": -99.3300, "costo": 40},
    {"nombre": "QUERETARO-IRAPUATO", "lat": 20.5888, "lon": -100.3899, "costo": 85},
    {"nombre": "QUERETARO QUERETARO-CELAYA", "lat": 20.5870, "lon": -100.3900, "costo": 60},
    {"nombre": "APASEO QUERETARO-APASEO", "lat": 20.5110, "lon": -100.7300, "costo": 40},
    {"nombre": "APASEO APASEO-CELAYA", "lat": 20.5110, "lon": -100.7300, "costo": 45},
    {"nombre": "SALAMANCA CELAYA-SALAMANCA", "lat": 20.5690, "lon": -101.1920, "costo": 50},
    {"nombre": "SALAMANCA SALAMANCA-IRAPUATO", "lat": 20.5690, "lon": -101.1920, "costo": 45},
    {"nombre": "SALAMANCA CELAYA-IRAPUATO", "lat": 20.5700, "lon": -101.1900, "costo": 90},
    {"nombre": "VILLAGRAN VILLAGRAN-SALAMANCA", "lat": 20.5695, "lon": -101.1970, "costo": 35},
    {"nombre": "QUERETARO BIS QUERETARO-ENT.LIB. SUROESTE DE QRO.", "lat": 20.6000, "lon": -100.4000, "costo": 25},
    {"nombre": "QUERETARO BIS ENT.LIB. SUROESTE DE QRO.-CELAYA", "lat": 20.6000, "lon": -100.4000, "costo": 30},
    {"nombre": "CERRO GORDO CELAYA-ENT. CERRO GORDO", "lat": 20.5000, "lon": -100.8000, "costo": 35},
    {"nombre": "CERRO GORDO ENT. CERRO GORDO-IRAPUATO", "lat": 20.5150, "lon": -101.3650, "costo": 45},
    {"nombre": "CERRO GORDO ENT. CERRO GORDO-SALAMANCA", "lat": 20.5200, "lon": -101.1900, "costo": 40},
    {"nombre": "MEXICO-PUEBLA", "lat": 19.4326, "lon": -99.1332, "costo": 120},
    {"nombre": "CHALCO MEXICO-CHALCO", "lat": 19.2780, "lon": -98.8650, "costo": 30},
    {"nombre": "IXTAPALUCA CHALCO-MEXICO", "lat": 19.2690, "lon": -98.8700, "costo": 25},
    {"nombre": "SAN MARCOS MEXICO-SAN MARTIN TEXMELUCAN", "lat": 19.0630, "lon": -98.4120, "costo": 35},
    {"nombre": "SAN MARCOS BIS MEXICO-CIRCUITO EXTERIOR MEXIQUENSE", "lat": 19.0640, "lon": -98.4150, "costo": 40},
    {"nombre": "SAN MARTIN SAN MARTIN TEXMELUCAN-PUEBLA", "lat": 19.0500, "lon": -98.4000, "costo": 25},
    {"nombre": "PUEBLA-ACATZINGO", "lat": 18.9650, "lon": -98.3600, "costo": 20},
    {"nombre": "AMOZOC (D) PUEBLA-ACATZINGO", "lat": 19.0550, "lon": -98.2760, "costo": 15},
    {"nombre": "AMOZOC ( I ) PUEBLA-AMOZOC", "lat": 19.0570, "lon": -98.2750, "costo": 15},
    {"nombre": "ENT. AMOZOC III PUEBLA-ENT. (AMOZOC-PEROTE)", "lat": 19.0600, "lon": -98.2730, "costo": 20},

    {"nombre": "Oacalco A - Cuautla A", "lat": 18.6233, "lon": -98.8784, "costo": 12},
    {"nombre": "Cuautla B - Oacalco B", "lat": 18.6233, "lon": -98.8784, "costo": 12},
    {"nombre": "Oacalco A - Oaxtepec A", "lat": 18.6252, "lon": -98.9186, "costo": 10},
    {"nombre": "Oaxtepec B - Oacalco B", "lat": 18.6252, "lon": -98.9186, "costo": 10},
    {"nombre": "La Pera A - Oacalco A", "lat": 18.6540, "lon": -98.8741, "costo": 18},
    {"nombre": "Oacalco B - La Pera B", "lat": 18.6540, "lon": -98.8741, "costo": 18},
    {"nombre": "La Pera A - Oaxtepec A", "lat": 18.6567, "lon": -98.9183, "costo": 14},
    {"nombre": "Oaxtepec B - La Pera B", "lat": 18.6567, "lon": -98.9183, "costo": 14},
    {"nombre": "Tepoztlán B - La Pera B", "lat": 18.8227, "lon": -99.0602, "costo": 20},
    {"nombre": "La Pera A - Tepoztlán A", "lat": 18.8227, "lon": -99.0602, "costo": 20},
    {"nombre": "Caseta México-Cuernavaca", "lat": 19.25, "lon": -99.21, "costo": 149.00},

    {"nombre": "Zacapalco - Rancho Viejo", "lat": 18.8710, "lon": -99.0689, "costo": 22},
    {"nombre": "Tihuatlán - Gutiérrez Zamora", "lat": 20.8507, "lon": -97.4980, "costo": 30},
    {"nombre": "Totomoxtle - Entr. El Pital", "lat": 20.8585, "lon": -97.4330, "costo": 28},
    {"nombre": "Entr. Tihuatlán - Puente Cazones", "lat": 20.8525, "lon": -97.4153, "costo": 25},
    {"nombre": "Puente Cazones - Entr. Totomoxtle", "lat": 20.8550, "lon": -97.4250, "costo": 25},
    {"nombre": "LOMAS VERDES-ATIZAPAN", "lat": 19.5910, "lon": -99.2520, "costo": 24},
    {"nombre": "LOMAS VERDES-MADIN", "lat": 19.5910, "lon": -99.2520, "costo": 17},
    {"nombre": "LOMAS VERDES-SAN MATEO NOPALA", "lat": 19.5910, "lon": -99.2520, "costo": 20},
    {"nombre": "LOMAS VERDES-CIPRESES", "lat": 19.5910, "lon": -99.2520, "costo": 25},
    {"nombre": "LOMAS VERDES-CHAMAPA", "lat": 19.6350, "lon": -99.3000, "costo": 32},
    {"nombre": "RETORNO LECHERIA RETORNO", "lat": 19.4916, "lon": -99.1637, "costo": 55},
    {"nombre": "ESTACION DON - NOGALES", "lat": 31.3072, "lon": -110.9443, "costo": 426},
    {"nombre": "ESTACION DON - NAVOJOA", "lat": 27.0775, "lon": -109.4639, "costo": 87},
    {"nombre": "FUNDICION NAVOJOA-CIUDAD OBREGON", "lat": 27.0775, "lon": -109.4639, "costo": 87},
    {"nombre": "ESPERANZA CIUDAD OBREGON-GUAYMAS", "lat": 27.4806, "lon": -110.3108, "costo": 87},
    {"nombre": "GUAYMAS LIBRAMIENTO GUAYMAS", "lat": 27.9191, "lon": -110.9031, "costo": 49},
    {"nombre": "HERMOSILLO HERMOSILLO-MAGDALENA DE KINO", "lat": 29.0728, "lon": -110.9559, "costo": 87},
    {"nombre": "MAGDALENA LIBRAMIENTO MAGDALENA DE KINO", "lat": 29.1692, "lon": -111.0207, "costo": 29},
    {"nombre": "LIB. CD. OBREGON (LICO) CIUDAD OBREGON-GUAYMAS", "lat": 27.4806, "lon": -110.3108, "costo": 79},
    {"nombre": "GOMEZ PALACIO-CORRALITOS-AUTOPISTA UNION", "lat": 25.5681, "lon": -103.4713, "costo": 203},
    {"nombre": "BERMEJILLO GOMEZ PALACIO-EST. BANDERAS", "lat": 25.4317, "lon": -103.3704, "costo": 98},
    {"nombre": "CEBALLOS EST. BANDERAS-CORRALITOS", "lat": 25.4320, "lon": -103.3700, "costo": 105},
    {"nombre": "TORREON -SALTILLO", "lat": 25.5394, "lon": -103.4500, "costo": 196},
    {"nombre": "LA CUCHILLA MATAMOROS-LA CUCHILLA", "lat": 25.5400, "lon": -103.4600, "costo": 73},
    {"nombre": "PLAN DE AYALA PLAN DE AYALA-EL PORVENIR", "lat": 25.6773, "lon": -100.3091, "costo": 123},
    {"nombre": "AGUA DULCE-CARDENAS", "lat": 18.0784, "lon": -93.1687, "costo": 81},
    {"nombre": "LA VENTA (AGUADULCE) (D) AGUADULCE-CARDENAS", "lat": 18.0784, "lon": -93.1687, "costo": 81},
    {"nombre": "LA VENTA (AGUADULCE) (I1) AGUADULCE-ENTR.MAGALLANES", "lat": 18.0784, "lon": -93.1687, "costo": 49},
    {"nombre": "LA VENTA (AGUADULCE) (I2) ENT. MAGALLANES-CARDENAS", "lat": 18.0880, "lon": -93.1535, "costo": 49},
    {"nombre": "MEXICO-CUERNAVACA", "lat": 19.3498, "lon": -99.2301, "costo": 137},
    {"nombre": "TLALPAN MEXICO-CUERNAVACA", "lat": 19.2966, "lon": -99.1823, "costo": 137},
    {"nombre": "TRES MARIAS 'A' Y 'B' TRES MARIAS-CUERNAVACA", "lat": 18.9534, "lon": -99.2306, "costo": 59},
    {"nombre": "PUENTE DE IXTLA-IGUALA", "lat": 18.6332, "lon": -99.2841, "costo": 108},
    {"nombre": "IGUALA PUENTE DE IXTLA-IGUALA", "lat": 18.6332, "lon": -99.2841, "costo": 108},
    {"nombre": "La Pera A - Cuautla A (Circuito cerrado)", "lat": 18.6926, "lon": -98.9411, "costo": 71},
    {"nombre": "Cuautla B - La Pera B", "lat": 18.6926, "lon": -98.9411, "costo": 71},
    {"nombre": "Tepoztlán Tepoztlán A - Oacalco A", "lat": 18.9766, "lon": -99.0976, "costo": 27},
    {"nombre": "Tepoztlán Oacalco B - Tepoztlán B", "lat": 18.9766, "lon": -99.0976, "costo": 26},
    {"nombre": "Tepoztlán Tepoztlán A - Cuautla A", "lat": 18.9766, "lon": -99.0976, "costo": 53},
    {"nombre": "Tepoztlán Cuautla B - Tepoztlán B", "lat": 18.9766, "lon": -99.0976, "costo": 53},
    {"nombre": "Tepoztlán Tepoztlán A - Oaxtepec A", "lat": 18.9806, "lon": -99.1036, "costo": 37},
    {"nombre": "Oaxtepec Oaxtepec B - Tepoztlán B", "lat": 18.9750, "lon": -99.1200, "costo": 36},
    {"nombre": "ACATZINGO-CD. MENDOZA", "lat": 18.9089, "lon": -97.0167, "costo": 73},
    {"nombre": "ESPERANZA (D) ACATZINGO-CD. MENDOZA", "lat": 18.9413, "lon": -97.0404, "costo": 73},
    {"nombre": "ESPERANZA (I1) ACATZINGO-ESPERANZA", "lat": 18.9409, "lon": -97.0400, "costo": 40},
    {"nombre": "ESPERANZA (I2) ESPERANZA-CD. MENDOZA", "lat": 18.9409, "lon": -97.0400, "costo": 40},
    {"nombre": "CIUDAD MENDOZA-CORDOBA", "lat": 18.8573, "lon": -97.0526, "costo": 73},
    {"nombre": "FORTIN (D) CD. MENDOZA-CORDOBA", "lat": 18.8604, "lon": -96.9953, "costo": 73},
    {"nombre": "FORTIN (I) CD. MENDOZA-FORTIN", "lat": 18.8623, "lon": -96.9708, "costo": 40},
    {"nombre": "TEHUACAN-OAXACA", "lat": 18.4559, "lon": -97.3865, "costo": 130},
    {"nombre": "TEHUACAN CUACNOPALAN-TEHUACAN", "lat": 18.4572, "lon": -97.3882, "costo": 65},
    {"nombre": "MIAHUATLAN TEHUACAN-MIAHUATLAN", "lat": 17.9958, "lon": -96.7503, "costo": 65},
    {"nombre": "SUCHIXTLAHUACA (D) MIAHUATLAN-NOCHIXTLAN", "lat": 17.9394, "lon": -97.0170, "costo": 70},
    {"nombre": "SUCHIXTLAHUACA (I) MIAHUATLAN-COIXTLAHUACA", "lat": 17.9394, "lon": -97.0170, "costo": 70},
    {"nombre": "HUITZO DIRECTA (D) NOCHIXTLAN-OAXACA", "lat": 17.0043, "lon": -96.7211, "costo": 65},
    {"nombre": "HUITZO INTERMEDIA (I1) NOCHIXTLAN-HUITZO", "lat": 17.0043, "lon": -96.7211, "costo": 50},
    {"nombre": "HUITZO BIS (I2) HUITZO-OAXACA", "lat": 17.0043, "lon": -96.7211, "costo": 40},
    {"nombre": "HUITZO (I3) HUITZO-NOCHIXTLAN", "lat": 17.0043, "lon": -96.7211, "costo": 40},
    {"nombre": "TIJUANA-ENSENADA", "lat": 32.5149, "lon": -117.0382, "costo": 151},
    {"nombre": "PLAYAS TIJUANA-ROSARITO", "lat": 32.5625, "lon": -117.0629, "costo": 55},
    {"nombre": "ROSARITO ROSARITO-LA MISION", "lat": 32.3583, "lon": -116.8828, "costo": 55},
    {"nombre": "NODO POPOTLA (I) LA MISIÓN-CORREDOR 2000", "lat": 32.5207, "lon": -116.9045, "costo": 55},
    {"nombre": "ENSENADA LA MISION-ENSENADA", "lat": 31.8688, "lon": -116.5963, "costo": 55},
    {"nombre": "RANCHO VIEJO-TAXCO", "lat": 18.5555, "lon": -99.6066, "costo": 62},
    {"nombre": "TAXCO RANCHO VIEJO-TAXCO", "lat": 18.5555, "lon": -99.6066, "costo": 62},
    {"nombre": "LA RUMOROSA-TECATE", "lat": 32.6765, "lon": -116.0344, "costo": 87},
    {"nombre": "EL HONGO (D) LA RUMOROSA-TECATE", "lat": 32.6765, "lon": -116.0344, "costo": 40},
    {"nombre": "EL HONGO (I) EL HONGO TECATE", "lat": 32.6562, "lon": -116.0291, "costo": 40},
    {"nombre": "EL HONGO (I2) LA RUMOROSA-EL HONGO", "lat": 32.6562, "lon": -116.0291, "costo": 40},
    {"nombre": "SAN JOSE DEL CABO AEROPUERTO LOS CABOS-SN. JOSE DEL CABO", "lat": 23.0667, "lon": -109.7000, "costo": 60},
    {"nombre": "AEROPUERTO LOS CABOS AEROPUERTO LOS CABOS-CABO SAN LUCAS", "lat": 23.1517, "lon": -109.7210, "costo": 90},
    {"nombre": "SAN JOSE DEL CABO SAN JOSE DEL CABO-CABO SAN LUCAS", "lat": 23.0611, "lon": -109.7072, "costo": 60},
    {"nombre": "SAN JOSE DEL CABO SAN JOSE DEL CABO-EL MANGLE", "lat": 23.0533, "lon": -109.7033, "costo": 30},
    {"nombre": "CABO SAN LUCAS CABO SAN LUCAS-EL MANGLE", "lat": 22.8906, "lon": -109.9011, "costo": 30},
    {"nombre": "SAN JOSE DEL CABO SAN JOSÉ DEL CABO-CABO REAL", "lat": 23.0644, "lon": -109.7050, "costo": 40},
    {"nombre": "AEROPUERTO LOS CABOS AEROPUERTO LOS CABOS-CABO REAL", "lat": 23.1533, "lon": -109.7200, "costo": 50},
    {"nombre": "AEROPUERTO LOS CABOS AEROPUERTO LOS CABOS-EL MANGLE", "lat": 23.1533, "lon": -109.7200, "costo": 30},
    {"nombre": "EL MANGLE EL MANGLE-CABO REAL", "lat": 23.0467, "lon": -109.6933, "costo": 30},
    {"nombre": "CABO REAL CABO REAL-CABO SAN LUCAS", "lat": 23.0000, "lon": -109.7000, "costo": 40},
    {"nombre": "AEROPUERTO LOS CABOS AEROP. LOS CABOS RETORNO", "lat": 23.1533, "lon": -109.7200, "costo": 0},
    {"nombre": "EL MANGLE EL MANGLE RETORNO", "lat": 23.0467, "lon": -109.6933, "costo": 0},
    {"nombre": "CABO SAN LUCAS CABO SAN LUCAS RETORNO", "lat": 22.8906, "lon": -109.9011, "costo": 0},
    {"nombre": "SAN JOSE DEL CABO SAN JOSE DEL CABO RETORNO", "lat": 23.0611, "lon": -109.7072, "costo": 0},
    {"nombre": "SALINA CRUZ-LA VENTOSA", "lat": 16.1667, "lon": -95.2000, "costo": 75},
    {"nombre": "TEHUANTEPEC (D) SALINA CRUZ-TEHUANTEPEC", "lat": 16.2667, "lon": -95.3500, "costo": 40},
    {"nombre": "IXTEPEC (D) TEHUANTEPEC-LA VENTOSA", "lat": 16.1500, "lon": -95.3833, "costo": 40},
    {"nombre": "IXTEPEC (I1) TEHUANTEPEC-IXTEPEC", "lat": 16.1500, "lon": -95.3833, "costo": 25},
    {"nombre": "IXTEPEC (I2) IXTEPEC-LA VENTOSA", "lat": 16.1500, "lon": -95.3833, "costo": 25},
    {"nombre": "LAS CHOAPAS-OCOZOCOAUTLA", "lat": 17.5426, "lon": -94.4232, "costo": 80},
    {"nombre": "LAS CHOAPAS (D) ENT. LAS CHOAPAS - ENT. NUEVO SACRIFICIO", "lat": 17.5370, "lon": -94.4310, "costo": 50},
    {"nombre": "LAS CHOAPAS (I1) ENT. LAS CHOAPAS - ENT. LAS CHOAPAS II", "lat": 17.5350, "lon": -94.4200, "costo": 40},
    {"nombre": "LAS CHOAPAS (I2) ENT.LAS CHOAPAS II - ENT.NUEVO SACRIFICIO", "lat": 17.5300, "lon": -94.4150, "costo": 40},
    {"nombre": "MALPASITO (D) ENT. NUEVO SACRIFICIO - ENT. RAUDALES", "lat": 17.5200, "lon": -94.4000, "costo": 45},
    {"nombre": "MALPASITO (I1) ENT. NUEVO SACRIFICIO - ENT. MALPASITO", "lat": 17.5150, "lon": -94.3950, "costo": 30},
    {"nombre": "MALPASITO (I2) ENT. MALPASITO - ENT. RAUDALES", "lat": 17.5100, "lon": -94.3900, "costo": 30},
    {"nombre": "OCOZOCOAUTLA (OCUILAPA) (D) ENT. RAUDALES - ENT. OCOZOCOAUTLA", "lat": 17.4750, "lon": -92.8900, "costo": 70},
    {"nombre": "MEXICO-QUERETARO", "lat": 19.4326, "lon": -99.1332, "costo": 142},
    {"nombre": "TEPOTZOTLAN MEXICO TEPEJI", "lat": 19.7854, "lon": -99.2815, "costo": 65},
    {"nombre": "JOROBAS JOROBAS-TEPEJI", "lat": 19.7660, "lon": -99.3400, "costo": 70},
    {"nombre": "JOROBAS (CEM) JOROBAS-TEPEJI", "lat": 19.7660, "lon": -99.3400, "costo": 70},
    {"nombre": "PALMILLAS TEPEJI-PALMILLAS", "lat": 19.7110, "lon": -99.3150, "costo": 50},
    {"nombre": "PALMILLAS BIS TEPEJI-PALMILLAS", "lat": 19.7110, "lon": -99.3150, "costo": 50},
    {"nombre": "POLOTITLAN TEPEJI-POLOTITLAN", "lat": 19.6750, "lon": -99.3300, "costo": 40},
    {"nombre": "QUERETARO-IRAPUATO", "lat": 20.5888, "lon": -100.3899, "costo": 70},
    {"nombre": "QUERETARO QUERETARO-CELAYA", "lat": 20.5870, "lon": -100.3900, "costo": 70},
    {"nombre": "APASEO QUERETARO-APASEO", "lat": 20.5110, "lon": -100.7300, "costo": 60},
    {"nombre": "APASEO APASEO-CELAYA", "lat": 20.5110, "lon": -100.7300, "costo": 60},
    {"nombre": "SALAMANCA CELAYA-SALAMANCA", "lat": 20.5690, "lon": -101.1920, "costo": 55},
    {"nombre": "SALAMANCA SALAMANCA-IRAPUATO", "lat": 20.5690, "lon": -101.1920, "costo": 55},
    {"nombre": "SALAMANCA CELAYA-IRAPUATO", "lat": 20.5700, "lon": -101.1900, "costo": 55},
    {"nombre": "VILLAGRAN VILLAGRAN-SALAMANCA", "lat": 20.5695, "lon": -101.1970, "costo": 50},
    {"nombre": "QUERETARO BIS QUERETARO-ENT.LIB. SUROESTE DE QRO.", "lat": 20.6000, "lon": -100.4000, "costo": 40},
    {"nombre": "QUERETARO BIS ENT.LIB. SUROESTE DE QRO.-CELAYA", "lat": 20.6000, "lon": -100.4000, "costo": 40},
    {"nombre": "CERRO GORDO CELAYA-ENT. CERRO GORDO", "lat": 20.5000, "lon": -100.8000, "costo": 30},
    {"nombre": "CERRO GORDO ENT. CERRO GORDO-IRAPUATO", "lat": 20.5150, "lon": -101.3650, "costo": 30},
    {"nombre": "CERRO GORDO ENT. CERRO GORDO-SALAMANCA", "lat": 20.5200, "lon": -101.1900, "costo": 30},
    {"nombre": "MEXICO-PUEBLA", "lat": 19.4326, "lon": -99.1332, "costo": 90},
    {"nombre": "CHALCO MEXICO-CHALCO", "lat": 19.2780, "lon": -98.8650, "costo": 35},
    {"nombre": "IXTAPALUCA CHALCO-MEXICO", "lat": 19.2690, "lon": -98.8700, "costo": 35},
    {"nombre": "SAN MARCOS MEXICO-SAN MARTIN TEXMELUCAN", "lat": 19.0630, "lon": -98.4120, "costo": 40},
    {"nombre": "SAN MARCOS BIS MEXICO-CIRCUITO EXTERIOR MEXIQUENSE", "lat": 19.0640, "lon": -98.4150, "costo": 40},
    {"nombre": "SAN MARTIN SAN MARTIN TEXMELUCAN-PUEBLA", "lat": 19.0500, "lon": -98.4000, "costo": 40},
    {"nombre": "PUEBLA-ACATZINGO", "lat": 18.9650, "lon": -98.3600, "costo": 40},
    {"nombre": "AMOZOC (D) PUEBLA-ACATZINGO", "lat": 19.0550, "lon": -98.2760, "costo": 25},
    {"nombre": "AMOZOC ( I ) PUEBLA-AMOZOC", "lat": 19.0570, "lon": -98.2750, "costo": 25},
    {"nombre": "ENT. AMOZOC III PUEBLA-ENT. (AMOZOC-PEROTE)", "lat": 19.0600, "lon": -98.2730, "costo": 25}
]

ubicaciones = []  # Lista global para puntos seleccionados (si usas)

@app.route('/')
def index():
    return render_template('index.html', casetas=casetas)

@app.route('/ruta', methods=['GET'])
def obtener_ruta():
    # Recibir puntos desde query params: ?p0=lat,lon&p1=lat,lon...
    puntos = []
    i = 0
    while True:
        param = request.args.get(f'p{i}')
        if not param:
            break
        try:
            lat_str, lon_str = param.split(',')
            puntos.append((float(lat_str), float(lon_str)))
        except:
            return jsonify(error="Parámetro de ubicación inválido"), 400
        i += 1

    if len(puntos) < 2:
        return jsonify(error="Se requieren al menos 2 ubicaciones"), 400

    ruta = calcular_ruta_optima_dijkstra(puntos)
    dist_km = calcular_distancia_km(ruta)
    gasolina_l = dist_km / 10  # Rendimiento 10 km/l
    costo_gas = gasolina_l * 24.53  # Precio gasolina por litro

    casetas_en_ruta = filtrado_casetas(ruta, casetas)
    total_casetas = sum(c['costo'] for c in casetas_en_ruta)

    velocidad_prom_kmh = 60  # Velocidad promedio para tiempo estimado
    tiempo_horas = dist_km / velocidad_prom_kmh

    return jsonify({
        "ruta": ruta,
        "distancia": round(dist_km, 2),
        "gasolina": round(gasolina_l, 2),
        "costoGasolina": round(costo_gas, 2),
        "casetas": casetas_en_ruta,
        "costoCasetas": round(total_casetas, 2),
        "totalViaje": round(costo_gas + total_casetas, 2),
        "tiempoHoras": round(tiempo_horas, 2)
    })

def calcular_distancia_km(ruta):
    total = 0
    for i in range(len(ruta) - 1):
        lat1, lon1 = ruta[i]
        lat2, lon2 = ruta[i + 1]
        # Distancia Manhattan entre puntos
        total += abs(lat1 - lat2) + abs(lon1 - lon2)
    return total * 111  # Aproximación km por grado

def calcular_ruta_optima_dijkstra(puntos):
    G = nx.Graph()
    for i, p in enumerate(puntos):
        G.add_node(i, pos=p)
    for i in range(len(puntos)):
        for j in range(i + 1, len(puntos)):
            dist = abs(puntos[i][0] - puntos[j][0]) + abs(puntos[i][1] - puntos[j][1])
            G.add_edge(i, j, weight=dist)
    path = nx.dijkstra_path(G, 0, len(puntos) - 1, weight='weight')
    return [puntos[i] for i in path]

def filtrado_casetas(ruta, casetas, umbral_km=2):
    seleccion = []
    for caseta in casetas:
        for pt in ruta:
            dist = haversine(pt, (caseta["lat"], caseta["lon"]))
            if dist <= umbral_km:
                seleccion.append(caseta)
                break
    return seleccion

def haversine(a, b):
    R = 6371  # km
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    return 2 * R * math.asin(math.sqrt(
        math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    ))

if __name__ == '__main__':
    app.run(debug=True)