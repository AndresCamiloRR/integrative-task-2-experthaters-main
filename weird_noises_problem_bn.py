from experta import *
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# Base de conocimiento para ruidos extraños
noise_problems = {
    "Noise Issues": {
        "symptoms": ["clunk_or_single_tick",
                     "Only_ticks_when_moving",
                     "time_bomb_under_seat",
                     "tick_neutral",
                     "tick_reverse",
                     "noisy_on_bombs",
                     "drops_on_shifts",
                     "ticks_on_turns",
                     "changed_tires",
                     "removed_hubcaps",
                     "inspect_tire_treads",
                     "ticks_slow_speed",
                     "ticks_cold",
                     "windshield_wipers_radio_off",
                     ],

        "general_causes": ["chasis_and_support_problems",
                           "Wheel_Issues",
                           "Transmission_Problems",
                           "Bearing_Problems",
                           "External_Noise"],

    }
}

model = BayesianNetwork([
    ('chasis_and_support_problems', 'clunk_or_single_tick'),
    ('chasis_and_support_problems', 'Only_ticks_when_moving'),
    ('chasis_and_support_problems', 'ticks_on_turns'),
    ('Wheel_Issues', 'changed_tires'),
    ('Wheel_Issues', 'removed_hubcaps'),
    ('Wheel_Issues', 'inspect_tire_treads'),
    ('Wheel_Issues', 'ticks_slow_speed'),
    ('Transmission_Problems', 'tick_neutral'),
    ('Transmission_Problems', 'tick_reverse'),
    ('Transmission_Problems', 'drops_on_shifts'),
    ('Bearing_Problems', 'time_bomb_under_seat'),
    ('Bearing_Problems', 'noisy_on_bombs'),
    ('External_Noise', 'windshield_wipers_radio_off'),
    ('External_Noise', 'ticks_cold')
])

cpd_suspension = TabularCPD(
    variable='chasis_and_support_problems',
    variable_card=2,
    values=[[0.85], [0.15]]
)

cpd_wheel = TabularCPD(
    variable='Wheel_Issues',
    variable_card=2,
    values=[[0.80], [0.20]]
)

cpd_transmission = TabularCPD(
    variable='Transmission_Problems',
    variable_card=2,
    values=[[0.90], [0.10]]
)

cpd_bearing = TabularCPD(
    variable='Bearing_Problems',
    variable_card=2,
    values=[[0.95], [0.05]]
)

cpd_external = TabularCPD(
    variable='External_Noise',
    variable_card=2,
    values=[[0.70], [0.30]]
)

cpd_clunk = TabularCPD(
    variable='clunk_or_single_tick',
    variable_card=2,
    evidence=['chasis_and_support_problems'],
    evidence_card=[2],
    values=[[0.9, 0.2],
            [0.1, 0.8]]
)

cpd_ticks_moving = TabularCPD(
    variable='Only_ticks_when_moving',
    variable_card=2,
    evidence=['chasis_and_support_problems'],
    evidence_card=[2],
    values=[[0.95, 0.15],
            [0.05, 0.85]]
)

cpd_ticks_turns = TabularCPD(
    variable='ticks_on_turns',
    variable_card=2,
    evidence=['chasis_and_support_problems'],
    evidence_card=[2],
    values=[[0.85, 0.25],
            [0.15, 0.75]]
)

cpd_changed_tires = TabularCPD(
    variable='changed_tires',
    variable_card=2,
    evidence=['Wheel_Issues'],
    evidence_card=[2],
    values=[[0.95, 0.3],
            [0.05, 0.7]]
)

cpd_hubcaps = TabularCPD(
    variable='removed_hubcaps',
    variable_card=2,
    evidence=['Wheel_Issues'],
    evidence_card=[2],
    values=[[0.9, 0.4],
            [0.1, 0.6]]
)

cpd_treads = TabularCPD(
    variable='inspect_tire_treads',
    variable_card=2,
    evidence=['Wheel_Issues'],
    evidence_card=[2],
    values=[[0.8, 0.2],
            [0.2, 0.8]]
)

cpd_slow_speed = TabularCPD(
    variable='ticks_slow_speed',
    variable_card=2,
    evidence=['Wheel_Issues'],
    evidence_card=[2],
    values=[[0.9, 0.3],
            [0.1, 0.7]]
)

cpd_neutral = TabularCPD(
    variable='tick_neutral',
    variable_card=2,
    evidence=['Transmission_Problems'],
    evidence_card=[2],
    values=[[0.95, 0.2],
            [0.05, 0.8]]
)

cpd_reverse = TabularCPD(
    variable='tick_reverse',
    variable_card=2,
    evidence=['Transmission_Problems'],
    evidence_card=[2],
    values=[[0.9, 0.15],
            [0.1, 0.85]]
)

cpd_shifts = TabularCPD(
    variable='drops_on_shifts',
    variable_card=2,
    evidence=['Transmission_Problems'],
    evidence_card=[2],
    values=[[0.85, 0.1],
            [0.15, 0.9]]
)

cpd_time_bomb = TabularCPD(
    variable='time_bomb_under_seat',
    variable_card=2,
    evidence=['Bearing_Problems'],
    evidence_card=[2],
    values=[[0.98, 0.15],
            [0.02, 0.85]]
)

cpd_bombs = TabularCPD(
    variable='noisy_on_bombs',
    variable_card=2,
    evidence=['Bearing_Problems'],
    evidence_card=[2],
    values=[[0.95, 0.2],
            [0.05, 0.8]]
)

cpd_wipers = TabularCPD(
    variable='windshield_wipers_radio_off',
    variable_card=2,
    evidence=['External_Noise'],
    evidence_card=[2],
    values=[[0.9, 0.3],
            [0.1, 0.7]]
)

cpd_cold = TabularCPD(
    variable='ticks_cold',
    variable_card=2,
    evidence=['External_Noise'],
    evidence_card=[2],
    values=[[0.85, 0.25],
            [0.15, 0.75]]
)

model.add_cpds(cpd_suspension, cpd_wheel, cpd_transmission, cpd_bearing, cpd_external,
               cpd_clunk, cpd_ticks_moving, cpd_ticks_turns,
               cpd_changed_tires, cpd_hubcaps, cpd_treads, cpd_slow_speed,
               cpd_neutral, cpd_reverse, cpd_shifts,
               cpd_time_bomb, cpd_bombs,
               cpd_wipers, cpd_cold)

assert model.check_model()

inference = VariableElimination(model)


class SintomaVehiculo(Fact):
    """Síntomas del vehículo"""
    pass


class DiagnosisRuidos(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnosis = []
        self.recommendations = []

    @DefFacts()
    def hechos_iniciales_ruidos(self):
        yield Fact(sintoma="clunk_or_single_tick", descripcion="Golpes o un solo clic al moverse.")
        yield Fact(sintoma="Only_ticks_when_moving", descripcion="Ruidos que solo se escuchan mientras el vehículo está en movimiento.")
        yield Fact(sintoma="time_bomb_under_seat", descripcion="Ruido similar a una bomba de tiempo debajo del asiento.")
        yield Fact(sintoma="tick_neutral", descripcion="Clics o ruidos presentes cuando el vehículo está en neutral.")
        yield Fact(sintoma="tick_reverse", descripcion="Clics o ruidos al engranar la reversa.")
        yield Fact(sintoma="noisy_on_bombs", descripcion="Ruidos al pasar por baches o desniveles.")
        yield Fact(sintoma="drops_on_shifts", descripcion="Caídas o ruidos durante los cambios de marcha.")
        yield Fact(sintoma="ticks_on_turns", descripcion="Ruidos o clics al girar el vehículo.")
        yield Fact(sintoma="changed_tires", descripcion="Se cambiaron los neumáticos recientemente.")
        yield Fact(sintoma="removed_hubcaps", descripcion="Tapacubos removidos, lo que puede generar ruidos.")
        yield Fact(sintoma="inspect_tire_treads", descripcion="Necesidad de inspeccionar el desgaste de las llantas.")
        yield Fact(sintoma="ticks_slow_speed", descripcion="Ruidos que ocurren a baja velocidad.")
        yield Fact(sintoma="ticks_cold", descripcion="Ruidos que solo se escuchan cuando el motor está frío.")
        yield Fact(sintoma="windshield_wipers_radio_off", descripcion="Ruidos provenientes de limpiaparabrisas u otros accesorios externos.")
        yield Fact(sintoma="chasis_and_support_problems", descripcion="Problemas en el chasis y soportes del vehículo.")
        yield Fact(sintoma="Wheel_Issues", descripcion="Problemas relacionados con las ruedas.")
        yield Fact(sintoma="Transmission_Problems", descripcion="Problemas asociados con la transmisión del vehículo.")
        yield Fact(sintoma="Bearing_Problems", descripcion="Fallas en los rodamientos del vehículo.")
        yield Fact(sintoma="External_Noise", descripcion="Ruidos externos causados por accesorios o componentes sueltos.")

    def get_recommendation(self, diagnosis):
        recommendations = {
            "Problema de suspensión": "Recomendación: Verifique los componentes de suspensión, incluidos los struts, shocks y resortes. Inspeccione las soldaduras y asegure que las conexiones estén firmes.",
            "Problema de dirección o soportes del motor": "Recomendación: Inspeccione las rótulas, los soportes del motor, los frenos y la cremallera de dirección. Ajuste o reemplace componentes defectuosos.",
            "Problema en motor o escape": "Recomendación: Use herramientas de diagnóstico como un estetoscopio mecánico para localizar el ruido. Verifique el estado del sistema de escape.",
            "Problema de transmisión": "Recomendación: Revise el nivel y calidad del fluido de transmisión. Cambie el filtro si es necesario.",
            "Problema con el ajustador del freno trasero": "Recomendación: Inspeccione y ajuste los frenos traseros. Verifique que los tambores y las zapatas estén en buen estado.",
            "Problema en ruedas tras cambio reciente": "Recomendación: Confirme que las ruedas están bien instaladas y ajustadas. Realice un balanceo si es necesario.",
            "Problema en rodamientos": "Recomendación: Use un estetoscopio mecánico para localizar el ruido. Reemplace los rodamientos defectuosos lo antes posible.",
            "Ruido externo": "Recomendación: Verifique limpiaparabrisas, antenas y otros accesorios. Ajuste o reemplace componentes sueltos.",
            "Problema en neumáticos": "Recomendación: Revise los neumáticos en busca de desgaste irregular u objetos incrustados. Considere un alineamiento.",
            "Problema en amortiguadores": "Recomendación: Inspeccione los amortiguadores y reemplace aquellos que muestren desgaste.",
            "Problema en juntas CV o homocinéticas": "Recomendación: Revise las juntas CV por desgaste. Reemplace las juntas o lubrique si es necesario.",
            "Problema en sistema de escape frío": "Recomendación: Inspeccione los soportes del escape y el sistema en su conjunto cuando el motor esté frío.",
            "Problema de alineación en neumáticos": "Recomendación: Realice un alineamiento de las ruedas para corregir el desgaste irregular.",
            "Falla severa en rodamientos": "Recomendación: Reemplace los rodamientos inmediatamente. Evite usar el vehículo hasta que se repare.",
            "Problema de fluido de transmisión": "Recomendación: Cambie el fluido de transmisión y verifique si el problema persiste. Realice un servicio completo si es necesario.",
            "Problema eléctrico": "Recomendación: Inspeccione todas las conexiones eléctricas y asegúrese de que no haya cables sueltos o dañados.",
            "Múltiples problemas en suspensión": "Recomendación: Inspeccione la suspensión completa, incluidos todos los componentes principales. Considere un servicio profesional.",
            "Problema en instalación de neumáticos": "Recomendación: Confirme que los neumáticos están correctamente instalados y balanceados.",
            "Problema en engranajes de reversa": "Recomendación: Inspeccione el sistema de cambios, especialmente el mecanismo de reversa.",
            "Problema en retenedores de tapacubos": "Recomendación: Ajuste o reemplace los retenedores de los tapacubos para eliminar ruidos.",
            "Problema en catalizador o escape": "Recomendación: Inspeccione el sistema de escape y el catalizador. Repare o reemplace componentes defectuosos.",
            "Problema general en transmisión": "Recomendación: Realice un diagnóstico completo de la transmisión. Consulte a un especialista.",
            "Problema en balanceo de ruedas": "Recomendación: Lleve las ruedas a un taller para realizar un balanceo profesional.",
            "Problema en objetos incrustados en neumáticos": "Recomendación: Retire objetos extraños incrustados en los neumáticos y repare si es necesario.",
            "Problemas múltiples en fuentes externas": "Recomendación: Inspeccione de forma sistemática cada fuente de ruido externo. Ajuste o reemplace componentes dañados.",
            "Problema en dirección y rodamientos": "Recomendación: Revise los rodamientos de dirección. Reemplace componentes si es necesario.",
            "Problema en amortiguadores por ruido en baches": "Recomendación: Sustituya amortiguadores dañados. Inspeccione también resortes y soportes.",
            "Problema en dirección por ruido en curvas": "Recomendación: Verifique rótulas y extremos de la cremallera de dirección. Lubrique las piezas móviles.",
            "Problema combinado de suspensión y ruido": "Recomendación: Realice una inspección exhaustiva de la suspensión y dirección del vehículo.",
            "Revisar si las ruedas están bien ajustadas después del cambio.": "Recomendación: Confirme que las ruedas están bien instaladas y ajustadas. Realice un balanceo si es necesario.",
            "Revisar estado de los amortiguadores.": "Recomendación: Inspeccione los amortiguadores y reemplace aquellos que muestren desgaste."
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

    @Rule(
        SintomaVehiculo(name='clunk_or_single_tick') &
        SintomaVehiculo(name='noise_on_bumps')
    )
    def problema_suspension(self):
        diagnosis_text = "Diagnóstico: Problema de suspensión."
        result = inference.query(
            variables=['chasis_and_support_problems'],
            evidence={'clunk_or_single_tick': 1, 'noisy_on_bombs': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema de suspensión (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='clunk_or_single_tick') &
        ~SintomaVehiculo(name='noise_on_bumps')
    )
    def problema_direccion_soportes(self):
        diagnosis_text = "Diagnóstico: Revisar las rótulas, frenos, cremallera y extremos de las barras de dirección, soportes del motor."
        result = inference.query(
            variables=['chasis_and_support_problems'],
            evidence={'clunk_or_single_tick': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema de dirección/soportes (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        ~SintomaVehiculo(name='clunk_or_single_tick') &
        SintomaVehiculo(name='Only_ticks_when_moving') &
        SintomaVehiculo(name='tick_neutral') &
        SintomaVehiculo(name='drops_on_shifts')
    )
    def problema_motor_escape(self):
        diagnosis_text = "Diagnóstico: Intenta localizar el ruido con un tubo de escucha o un destornillador largo. El ruido parece ser del motor o del escape."
        result = inference.query(
            variables=['chasis_and_support_problems'],
            evidence={
                'Only_ticks_when_moving': 1,
                'tick_neutral': 1,
                'drops_on_shifts': 1
            }
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema del motor o escape (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='tick_neutral')
    )
    def problema_transmision_neutral(self):
        diagnosis_text = "Diagnóstico: Posible problema de transmisión. Revisar fluido y filtro."
        result = inference.query(
            variables=['Transmission_Problems'],
            evidence={'tick_neutral': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema de transmisión (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='tick_reverse')
    )
    def problema_freno_reversa(self):
        diagnosis_text = "Diagnóstico: Posible problema con el ajustador del freno trasero."
        result = inference.query(
            variables=['Transmission_Problems'],
            evidence={'tick_reverse': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en reversa (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='changed_tires') &
        SintomaVehiculo(name='ticks_on_turns')
    )
    def problema_ruedas_nuevas(self):
        diagnosis_text = "Diagnóstico: Revisar si las ruedas están bien ajustadas después del cambio."
        result = inference.query(
            variables=['Wheel_Issues'],
            evidence={'changed_tires': 1, 'ticks_on_turns': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en ruedas (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='time_bomb_under_seat')
    )
    def problema_rodamiento(self):
        diagnosis_text = "Diagnóstico: Revisar rodamientos. Usar estetoscopio para localizar."
        result = inference.query(
            variables=['Bearing_Problems'],
            evidence={'time_bomb_under_seat': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema de rodamientos (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='windshield_wipers_radio_off') &
        SintomaVehiculo(name='ticks_cold')
    )
    def ruido_externo(self):
        diagnosis_text = "Diagnóstico: Revisar fuentes de ruido externo (limpiaparabrisas, radio)."
        result = inference.query(
            variables=['External_Noise'],
            evidence={'windshield_wipers_radio_off': 1, 'ticks_cold': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de ruido externo (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='inspect_tire_treads') &
        SintomaVehiculo(name='ticks_slow_speed')
    )
    def problema_neumaticos(self):
        diagnosis_text = "Diagnóstico: Revisar desgaste de neumáticos y posibles objetos incrustados."
        result = inference.query(
            variables=['Wheel_Issues'],
            evidence={'inspect_tire_treads': 1, 'ticks_slow_speed': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en neumáticos (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='drops_on_shifts')
    )
    def problema_cambios_transmision(self):
        diagnosis_text = "Diagnóstico: Revisar sistema de transmisión durante los cambios."
        result = inference.query(
            variables=['Transmission_Problems'],
            evidence={'drops_on_shifts': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en transmisión (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='removed_hubcaps')
    )
    def problema_tapacubos(self):
        diagnosis_text = "Diagnóstico: Revisar ajuste de tapacubos y posibles problemas de retención."
        result = inference.query(
            variables=['Wheel_Issues'],
            evidence={'removed_hubcaps': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema con tapacubos (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='noisy_on_bombs')
    )
    def problema_amortiguacion(self):
        diagnosis_text = "Diagnóstico: Revisar sistema de amortiguación y componentes relacionados."
        result = inference.query(
            variables=['Bearing_Problems'],
            evidence={'noisy_on_bombs': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema de amortiguación (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='clunk_or_single_tick') &
        SintomaVehiculo(name='ticks_on_turns') &
        ~SintomaVehiculo(name='noise_on_bumps')
    )
    def problema_juntas_cv(self):
        diagnosis_text = "Diagnóstico: Posible desgaste en juntas CV o homocinéticas."
        result = inference.query(
            variables=['chasis_and_support_problems'],
            evidence={'clunk_or_single_tick': 1, 'ticks_on_turns': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en juntas (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='ticks_cold') &
        SintomaVehiculo(name='Only_ticks_when_moving')
    )
    def problema_escape_frio(self):
        diagnosis_text = "Diagnóstico: Revisar sistema de escape y soportes cuando está frío."
        result = inference.query(
            variables=['External_Noise'],
            evidence={'ticks_cold': 1, 'Only_ticks_when_moving': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en escape (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='inspect_tire_treads') &
        SintomaVehiculo(name='ticks_on_turns') &
        SintomaVehiculo(name='ticks_slow_speed')
    )
    def problema_desgaste_irregular(self):
        diagnosis_text = "Diagnóstico: Desgaste irregular en neumáticos, posible problema de alineación."
        result = inference.query(
            variables=['Wheel_Issues'],
            evidence={'inspect_tire_treads': 1, 'ticks_on_turns': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema de desgaste (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='time_bomb_under_seat') &
        SintomaVehiculo(name='Only_ticks_when_moving')
    )
    def problema_rodamiento_rueda(self):
        diagnosis_text = "Diagnóstico: Posible falla en rodamiento de rueda."
        result = inference.query(
            variables=['Bearing_Problems'],
            evidence={'time_bomb_under_seat': 1, 'Only_ticks_when_moving': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de falla en rodamiento (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='drops_on_shifts') &
        SintomaVehiculo(name='tick_neutral')
    )
    def problema_fluido_transmision(self):
        diagnosis_text = "Diagnóstico: Revisar nivel y calidad del fluido de transmisión."
        result = inference.query(
            variables=['Transmission_Problems'],
            evidence={'drops_on_shifts': 1, 'tick_neutral': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema de fluido (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='windshield_wipers_radio_off') &
        ~SintomaVehiculo(name='ticks_cold')
    )
    def problema_electrico(self):
        diagnosis_text = "Diagnóstico: Revisar sistema eléctrico y conexiones sueltas."
        result = inference.query(
            variables=['External_Noise'],
            evidence={'windshield_wipers_radio_off': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema eléctrico (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='clunk_or_single_tick') &
        SintomaVehiculo(name='noisy_on_bombs') &
        SintomaVehiculo(name='ticks_on_turns')
    )
    def problema_multiple_suspension(self):
        diagnosis_text = "Diagnóstico: Múltiples problemas en sistema de suspensión."
        result = inference.query(
            variables=['chasis_and_support_problems'],
            evidence={'clunk_or_single_tick': 1,
                      'noisy_on_bombs': 1, 'ticks_on_turns': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problemas múltiples (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='changed_tires') &
        SintomaVehiculo(name='ticks_slow_speed') &
        SintomaVehiculo(name='inspect_tire_treads')
    )
    def problema_instalacion_neumaticos(self):
        diagnosis_text = "Diagnóstico: Posible problema en la instalación de neumáticos nuevos."
        result = inference.query(
            variables=['Wheel_Issues'],
            evidence={'changed_tires': 1, 'ticks_slow_speed': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema de instalación (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='tick_reverse') &
        SintomaVehiculo(name='drops_on_shifts')
    )
    def problema_engranajes_reversa(self):
        diagnosis_text = "Diagnóstico: Revisar engranajes de reversa y mecanismo de cambios."
        result = inference.query(
            variables=['Transmission_Problems'],
            evidence={'tick_reverse': 1, 'drops_on_shifts': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en reversa (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='time_bomb_under_seat') &
        SintomaVehiculo(name='noisy_on_bombs') &
        SintomaVehiculo(name='Only_ticks_when_moving')
    )
    def problema_rodamiento_severo(self):
        diagnosis_text = "Diagnóstico: Falla severa en rodamientos, requiere atención inmediata."
        result = inference.query(
            variables=['Bearing_Problems'],
            evidence={'time_bomb_under_seat': 1, 'noisy_on_bombs': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de falla severa (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='clunk_or_single_tick') &
        SintomaVehiculo(name='Only_ticks_when_moving') &
        ~SintomaVehiculo(name='noise_on_bumps')
    )
    def problema_componentes_suspension(self):
        diagnosis_text = "Diagnóstico: Revisar componentes específicos de la suspensión."
        result = inference.query(
            variables=['chasis_and_support_problems'],
            evidence={'clunk_or_single_tick': 1, 'Only_ticks_when_moving': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en componentes (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='removed_hubcaps') &
        SintomaVehiculo(name='ticks_on_turns')
    )
    def problema_retenedor_tapacubos(self):
        diagnosis_text = "Diagnóstico: Revisar retenedores de tapacubos y ajuste."
        result = inference.query(
            variables=['Wheel_Issues'],
            evidence={'removed_hubcaps': 1, 'ticks_on_turns': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en retenedores (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='ticks_cold') &
        SintomaVehiculo(name='Only_ticks_when_moving') &
        ~SintomaVehiculo(name='windshield_wipers_radio_off')
    )
    def problema_escape_catalizador(self):
        diagnosis_text = "Diagnóstico: Revisar sistema de escape y catalizador."
        result = inference.query(
            variables=['External_Noise'],
            evidence={'ticks_cold': 1, 'Only_ticks_when_moving': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en escape (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='drops_on_shifts') &
        SintomaVehiculo(name='tick_neutral') &
        SintomaVehiculo(name='tick_reverse')
    )
    def problema_transmision_completo(self):
        diagnosis_text = "Diagnóstico: Problema general en la transmisión, requiere revisión completa."
        result = inference.query(
            variables=['Transmission_Problems'],
            evidence={'drops_on_shifts': 1,
                      'tick_neutral': 1, 'tick_reverse': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema general (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='inspect_tire_treads') &
        SintomaVehiculo(name='changed_tires') &
        SintomaVehiculo(name='ticks_on_turns')
    )
    def problema_balanceo_ruedas(self):
        diagnosis_text = "Diagnóstico: Posible problema de balanceo en las ruedas."
        result = inference.query(
            variables=['Wheel_Issues'],
            evidence={'inspect_tire_treads': 1, 'changed_tires': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema de balanceo (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='noisy_on_bombs') &
        SintomaVehiculo(name='Only_ticks_when_moving')
    )
    def problema_amortiguadores(self):
        diagnosis_text = "Diagnóstico: Revisar estado de los amortiguadores."
        result = inference.query(
            variables=['chasis_and_support_problems'],
            evidence={'noisy_on_bombs': 1, 'Only_ticks_when_moving': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en amortiguadores (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='ticks_slow_speed') &
        SintomaVehiculo(name='inspect_tire_treads') &
        ~SintomaVehiculo(name='changed_tires')
    )
    def problema_objetos_neumaticos(self):
        diagnosis_text = "Diagnóstico: Buscar objetos incrustados en los neumáticos."
        result = inference.query(
            variables=['Wheel_Issues'],
            evidence={'ticks_slow_speed': 1, 'inspect_tire_treads': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de objetos extraños (P={prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='windshield_wipers_radio_off') &
        SintomaVehiculo(name='ticks_cold') &
        SintomaVehiculo(name='Only_ticks_when_moving')
    )
    def problema_multiple_externo(self):
        diagnosis_text = "Diagnóstico: Múltiples fuentes de ruido externo, requiere inspección sistemática."
        result = inference.query(
            variables=['External_Noise'],
            evidence={'windshield_wipers_radio_off': 1, 'ticks_cold': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de múltiples problemas (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)

    @Rule(
        SintomaVehiculo(name='time_bomb_under_seat') &
        SintomaVehiculo(name='ticks_on_turns') &
        SintomaVehiculo(name='Only_ticks_when_moving')
    )
    def problema_rodamiento_direccion(self):
        diagnosis_text = "Diagnóstico: Posible problema en rodamientos de dirección."
        result = inference.query(
            variables=['Bearing_Problems'],
            evidence={'time_bomb_under_seat': 1, 'ticks_on_turns': 1}
        )
        prob = result.values[1]
        diagnosis_text += f" Probabilidad de problema en dirección (P={
            prob:.2f})"
        self.__add_diagnosis(diagnosis_text)


def get_ruidos_problems_response(responses):
    engine = DiagnosisRuidos()
    engine.reset()

    symptoms_mapping = [
        'clunk_or_single_tick',
        'Only_ticks_when_moving',
        'time_bomb_under_seat',
        'tick_neutral',
        'tick_reverse',
        'noisy_on_bombs',
        'drops_on_shifts',
        'ticks_on_turns',
        'changed_tires',
        'removed_hubcaps',
        'inspect_tire_treads',
        'ticks_slow_speed',
        'ticks_cold',
        'windshield_wipers_radio_off'
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

        # Top 3 diagnósticos y recomendaciones
        top_diagnoses = sorted_diagnoses[:3]
        top_recommendations = sorted_recommendations[:3]

        response = "Resultados del diagnóstico de ruidos extraños:\n\n"
        response += "Top 3 Diagnósticos más probables:\n"
        for i, (diagnosis, recommendation) in enumerate(zip(top_diagnoses, top_recommendations), 1):
            response += f"{i}. {diagnosis}\n   {recommendation}\n"

        if len(sorted_diagnoses) > 3:
            response += "\nNota: Se encontraron diagnósticos adicionales. Consulte un mecánico para una evaluación completa."

        return response
    else:
        return "No se encontraron problemas específicos relacionados con ruidos con la información proporcionada. Se recomienda una revisión presencial si los síntomas persisten."
