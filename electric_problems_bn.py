from experta import *
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

model = BayesianNetwork([
    ('Battery', 'ElectricalFailure'),
    ('Alternator', 'ElectricalFailure'),
    ('Wiring', 'ElectricalFailure'),
    ('Fuses', 'ElectricalFailure'),
    ('ElectricalFailure', 'HeadlightIssues'),
    ('ElectricalFailure', 'StartingIssues'),
    ('ElectricalFailure', 'RecommendationElectrical')
])

cpd_battery = TabularCPD(
    variable='Battery',
    variable_card=2,
    values=[[0.75], [0.25]]
)

cpd_alternator = TabularCPD(
    variable='Alternator',
    variable_card=2,
    values=[[0.8], [0.2]]
)

cpd_wiring = TabularCPD(
    variable='Wiring',
    variable_card=2,
    values=[[0.85], [0.15]]
)

cpd_fuses = TabularCPD(
    variable='Fuses',
    variable_card=2,
    values=[[0.9], [0.1]]
)

cpd_electrical_failure = TabularCPD(
    variable='ElectricalFailure',
    variable_card=2,
    values=[[0.95, 0.85, 0.75, 0.65, 0.6, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05, 0.02],
            [0.05, 0.15, 0.25, 0.35, 0.4, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.98]],
    evidence=['Battery', 'Alternator', 'Wiring', 'Fuses'],
    evidence_card=[2, 2, 2, 2]
)


cpd_headlight_issues = TabularCPD(
    variable='HeadlightIssues',
    variable_card=2,
    values=[[0.9, 0.3], [0.1, 0.7]],
    evidence=['ElectricalFailure'],
    evidence_card=[2]
)

cpd_starting_issues = TabularCPD(
    variable='StartingIssues',
    variable_card=2,
    values=[[0.85, 0.2], [0.15, 0.8]],
    evidence=['ElectricalFailure'],
    evidence_card=[2]
)

cpd_recommendation_electrical = TabularCPD(
    variable='RecommendationElectrical',
    variable_card=3,
    values=[[0.7, 0.2],
            [0.2, 0.5],
            [0.1, 0.3]],
    evidence=['ElectricalFailure'],
    evidence_card=[2]
)

model.add_cpds(
    cpd_battery, cpd_alternator, cpd_wiring, cpd_fuses,
    cpd_electrical_failure, cpd_headlight_issues, cpd_starting_issues,
    cpd_recommendation_electrical
)

assert model.check_model()


# Inference
inference = VariableElimination(model)


class SintomaVehiculo(Fact):
    """Síntomas del vehículo"""
    pass


class DiagnosisElectrico(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnosis = []
        self.recommendations = []

    @DefFacts()
    def inicializar_sintomas_comunes(self):
        yield Fact(sintoma="Battery", descripcion="La batería suele ser la causa principal de problemas eléctricos en los vehículos.")
        yield Fact(sintoma="Alternator", descripcion="El alternador puede fallar, especialmente en vehículos antiguos o con alto kilometraje.")
        yield Fact(sintoma="Wiring", descripcion="El cableado defectuoso es común en vehículos que han sufrido modificaciones eléctricas.")
        yield Fact(sintoma="Fuses", descripcion="Fusibles fundidos ocurren debido a cortocircuitos o sobrecargas en el sistema eléctrico.")
        yield Fact(sintoma="HeadlightIssues", descripcion="Problemas con las luces frontales, como parpadeo o atenuación.")
        yield Fact(sintoma="StartingIssues", descripcion="Dificultades para encender el vehículo, especialmente en clima frío.")
        yield Fact(sintoma="ElectricalFailure", descripcion="Fallas eléctricas generales que afectan múltiples sistemas en el vehículo.")

    def get_recommendation(self, diagnosis):
        recommendations = {
            "Problema en la batería": "Recomendación: Realice una prueba de carga de batería. Recargue o reemplace la batería si su capacidad es inferior al 70%. Verifique los terminales en busca de corrosión y límpielos si es necesario.",
            "Problema en el alternador": "Recomendación: Haga una prueba de voltaje del alternador. Verifique las correas de transmisión en busca de desgaste. Si el voltaje es bajo, considere reemplazar el alternador.",
            "Cableado defectuoso": "Recomendación: Inspeccione visualmente todo el cableado en busca de cables desgastados, quemados o agrietados. Use un multímetro para verificar continuidad. Reemplace cualquier cable dañado y asegure todas las conexiones.",
            "Fusibles fundidos": "Recomendación: Localice la caja de fusibles y reemplace todos los fusibles dañados con fusibles del mismo amperaje. Investigue la causa del cortocircuito antes de reemplazarlos.",
            "Problema en luces causado por batería débil": "Recomendación: Cargue la batería completamente. Verifique la intensidad de las luces. Si persiste el problema, revise los conectores de las luces y el interruptor.",
            "Dificultad para encender debido a batería débil": "Recomendación: Realice una prueba de arranque. Utilice cables puente para verificar si el problema es solo de batería. Considere reemplazar la batería si no mantiene la carga.",
            "Fallo eléctrico total": "Recomendación: Realice un diagnóstico integral del sistema eléctrico. Verifique batería, alternador, cableado y fusibles. Es probable que requiera servicio profesional.",
            "Alternador defectuoso afectando las luces": "Recomendación: Pruebe el voltaje del alternador. Verifique la tensión de la correa. Si el voltaje es inestable, reemplace el alternador.",
            "Fusibles dañados causando problemas en las luces": "Recomendación: Revise y reemplace los fusibles relacionados con el circuito de iluminación. Verifique que no haya cortocircuitos.",
            "Problema en el cableado afectando el arranque": "Recomendación: Inspeccione el cableado del sistema de arranque. Verifique conexiones en el motor de arranque y el interruptor de encendido.",
            "Problema con la batería y fusibles defectuosos": "Recomendación: Revise simultáneamente la batería y la caja de fusibles. Reemplace fusibles y realice prueba de carga de batería.",
            "Falla eléctrica relacionada con el alternador": "Recomendación: Verifique el voltaje de salida del alternador. Compruebe las conexiones y la condición de las correas.",
            "Luces parpadeantes debido a cableado defectuoso": "Recomendación: Realice una inspección detallada del cableado de iluminación. Busque conexiones sueltas o dañadas.",
            "Falla total debido a fusibles defectuosos": "Recomendación: Reemplace todos los fusibles. Investigue la causa fundamental de la sobrecarga o cortocircuito.",
            "Problemas combinados en batería, alternador y cableado": "Recomendación: Se requiere diagnóstico profesional completo. Los problemas múltiples sugieren una falla sistémica que necesita revisión integral."
        }

        for key, recommendation in recommendations.items():
            if key in diagnosis:
                return recommendation

        return recommendations.get(diagnosis, "Recomendación general: Consulte a un mecánico especialista para un diagnóstico detallado.")

    def __add_diagnosis(self, diagnosis_text):
        if diagnosis_text not in self.diagnosis:
            self.diagnosis.append(diagnosis_text)
            recommendation = self.get_recommendation(diagnosis_text)
            self.recommendations.append(recommendation)

    @Rule(SintomaVehiculo(name='Battery'))
    def problema_bateria_general(self):
        diagnosis_text = "Diagnóstico: Problema en la batería. Revisa el estado de carga o reemplaza si es necesario."
        result = inference.query(
            variables=['ElectricalFailure'], evidence={'Battery': 1})
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de falla en batería (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(SintomaVehiculo(name='Alternator'))
    def problema_alternador_general(self):
        diagnosis_text = "Diagnóstico: Problema en el alternador. Verifica el voltaje de salida."
        result = inference.query(
            variables=['ElectricalFailure'], evidence={'Alternator': 1})
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de falla en alternador (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(SintomaVehiculo(name='Wiring'))
    def problema_cableado_general(self):
        diagnosis_text = "Diagnóstico: Cableado defectuoso. Revisa conexiones y puntos de calentamiento."
        result = inference.query(
            variables=['ElectricalFailure'], evidence={'Wiring': 1})
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de falla en cableado (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(SintomaVehiculo(name='Fuses'))
    def problema_fusibles_generales(self):
        diagnosis_text = "Diagnóstico: Fusibles fundidos. Reemplaza fusibles dañados."
        result = inference.query(
            variables=['ElectricalFailure'], evidence={'Fuses': 1})
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en fusibles (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(SintomaVehiculo(name='HeadlightIssues') & SintomaVehiculo(name='Battery'))
    def problema_luces_y_bateria(self):
        diagnosis_text = "Diagnóstico: Problema en luces causado por batería débil."
        result = inference.query(
            variables=['HeadlightIssues'], evidence={'Battery': 1})
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en luces (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(SintomaVehiculo(name='StartingIssues') & SintomaVehiculo(name='Battery'))
    def problema_arranque_bateria(self):
        diagnosis_text = "Diagnóstico: Dificultad para encender debido a batería débil o descargada."
        result = inference.query(
            variables=['StartingIssues'], evidence={'Battery': 1})
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en arranque (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(SintomaVehiculo(name='ElectricalFailure') & SintomaVehiculo(name='Battery') & SintomaVehiculo(name='Alternator'))
    def problema_falla_electrica_total(self):
        diagnosis_text = "Diagnóstico: Fallo eléctrico total. Verifica batería, alternador y conexiones."
        result = inference.query(variables=['ElectricalFailure'], evidence={
                                 'Battery': 1, 'Alternator': 1})
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de falla eléctrica total (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(SintomaVehiculo(name='HeadlightIssues') & SintomaVehiculo(name='Alternator'))
    def problema_alternador_luces(self):
        diagnosis_text = "Diagnóstico: Alternador defectuoso afectando las luces del vehículo."
        result = inference.query(
            variables=['HeadlightIssues'], evidence={'Alternator': 1})
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en alternador (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(SintomaVehiculo(name='HeadlightIssues') & SintomaVehiculo(name='Fuses'))
    def problema_fusibles_luces(self):
        diagnosis_text = "Diagnóstico: Fusibles dañados causando problemas en las luces."
        result = inference.query(
            variables=['HeadlightIssues'], evidence={'Fuses': 1})
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en fusibles (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(SintomaVehiculo(name='StartingIssues') & SintomaVehiculo(name='Wiring'))
    def problema_cableado_arranque(self):
        diagnosis_text = "Diagnóstico: Problema en el cableado afectando el arranque del motor."
        result = inference.query(
            variables=['StartingIssues'], evidence={'Wiring': 1})
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en cableado (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(SintomaVehiculo(name='Battery') & SintomaVehiculo(name='Fuses'))
    def problema_bateria_fusibles(self):
        diagnosis_text = "Diagnóstico: Problema con la batería y fusibles defectuosos."
        result = inference.query(variables=['ElectricalFailure'], evidence={
                                 'Battery': 1, 'Fuses': 1})
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de falla en batería y fusibles (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(SintomaVehiculo(name='ElectricalFailure') & SintomaVehiculo(name='Alternator'))
    def problema_electrico_alternador(self):
        diagnosis_text = "Diagnóstico: Falla eléctrica relacionada con el alternador."
        result = inference.query(
            variables=['ElectricalFailure'], evidence={'Alternator': 1})
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de falla eléctrica (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(SintomaVehiculo(name='HeadlightIssues') & SintomaVehiculo(name='Wiring'))
    def problema_cableado_luces(self):
        diagnosis_text = "Diagnóstico: Luces parpadeantes debido a cableado defectuoso."
        result = inference.query(
            variables=['HeadlightIssues'], evidence={'Wiring': 1})
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en cableado (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(SintomaVehiculo(name='ElectricalFailure') & SintomaVehiculo(name='Fuses'))
    def problema_fallo_fusibles(self):
        diagnosis_text = "Diagnóstico: Falla total debido a fusibles defectuosos."
        result = inference.query(
            variables=['ElectricalFailure'], evidence={'Fuses': 1})
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de falla eléctrica por fusibles (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(SintomaVehiculo(name='Battery') & SintomaVehiculo(name='Alternator') & SintomaVehiculo(name='Wiring'))
    def problema_multiples_fallas(self):
        diagnosis_text = "Diagnóstico: Problemas combinados en batería, alternador y cableado."
        result = inference.query(variables=['ElectricalFailure'], evidence={
                                 'Battery': 1, 'Alternator': 1, 'Wiring': 1})
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de múltiples fallas (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)


def get_electric_problems_response(responses):
    engine = DiagnosisElectrico()
    engine.reset()

    symptoms_mapping = [
        'Battery',
        'Alternator',
        'Wiring',
        'Fuses',
        'HeadlightIssues',
        'StartingIssues',
        'ElectricalFailure'
    ]

    for i, response in enumerate(responses):
        if response == 's':
            engine.declare(SintomaVehiculo(name=symptoms_mapping[i]))

    engine.run()

    if engine.diagnosis:
        sorted_diagnoses = sorted(
            engine.diagnosis,
            key=lambda x: float(
                x.split('(P=')[-1].strip(')')) if '(P=' in x else 0,
            reverse=True
        )

        sorted_recommendations = [
            engine.get_recommendation(diagnosis)
            for diagnosis in sorted_diagnoses
        ]

        top_diagnoses = sorted_diagnoses[:3]
        top_recommendations = sorted_recommendations[:3]

        response = "Resultados del diagnóstico eléctrico:\n\n"
        response += "Top 3 Diagnósticos más probables:\n"
        for i, (diagnosis, recommendation) in enumerate(zip(top_diagnoses, top_recommendations), 1):
            response += f"{i}. {diagnosis}\n   {recommendation}\n"

        if len(sorted_diagnoses) > 3:
            response += "\nNota: Se encontraron diagnósticos adicionales. Consulte un mecánico para una evaluación completa."

        return response
    else:
        return "No se pudo determinar el problema con la información proporcionada. Se recomienda una revisión presencial."