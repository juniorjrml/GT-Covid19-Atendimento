from datetime import datetime
from dao.atendimento import AtendimentoBuilder
from dao.paciente import inserirPaciente
from flask_login import current_user
from controller.formfuncs import *


def registrar(form):
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    data = datetime.today()
    # ============== Paciente ==============

    nome = data_or_null(form['nome'])
    cpf = data_or_null(form['cpf'], only_num)
    cns = data_or_null(form['cns'], only_num)
    telefone = data_or_null(form['telefone'], only_num)
    endereco = data_or_null(form['endereco'])
    data_nasc = datetime.strptime(form['data_nasc'], '%d/%m/%Y').date() if len(form['data_nasc']) != 0 else None
    id_etnia = data_or_null(form['id_etnia'], int)
    id_genero = data_or_null(form['id_genero'], int)

    print('nome: {}'.format(nome))
    print('cpf: {}'.format(cpf))
    print('cns: {}'.format(cns))
    print('telefone: {}'.format(telefone))
    print('endereco: {}'.format(endereco))
    print('data_nasc: {}'.format(data_nasc))
    print('id_etnia: {}'.format(id_etnia))
    print('id_genero: {}'.format(id_genero))

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    id_paciente = inserirPaciente(nome, cpf, cns, telefone, endereco, data_nasc, id_etnia, id_genero, current_user.id_cidade)

    id_admsaude = current_user.id
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    builder = None
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    print('atendimento: ' + form['has_atendimento'])

    has_atendimento = True if form['has_atendimento'] == '1' else False

    print('has_atendimento: {}'.format(has_atendimento))

    if not has_atendimento:

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # builder = AtendimentoBuilder(True, data, id_paciente, None)
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

        # ============ Tentativa ============

        # Comentei algumas coisas porque aparentemente so teremos uma tentativa

        raw_tentativas = form['tentativas'].split(',')

        # Retorna as chaves da tabela de dom??nio (list<int>)
        # ex.: [0, 1]
        real_tentativas = get_real_data(raw_tentativas)
        # real_tentativas = data_or_null(form['tentativas'])

        print('real_tentativas: {}'.format(real_tentativas))

        # Retorna as outras op????es que n??o est??o na tabela de dom??nio (list<str>)
        # ex.: ['Paciente saiu para buscar o filho na escola']
        others_tentativas = get_others_data(raw_tentativas)

        print('others_tentativas: {}'.format(others_tentativas))

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        builder = AtendimentoBuilder(True, data, id_paciente, has_atendimento, tentativa=real_tentativas, others_tentativas = others_tentativas)
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    else:
        
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        builder = AtendimentoBuilder(True, data, id_paciente, has_atendimento)
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

        # ============== Doen??a Cronica ==============

        has_doenca_cronica = data_or_null(form['has_doenca_cronica'], int)

        if has_doenca_cronica == 1:  # Sim
            size = data_or_null(form['has_doenca_cronica_len'], int)

            real_doenca_cronica = multiselect(form, 'doenca_cronica', size)

            real_data_primeiro_sintoma = multiselect(form, 'data_primeiro_sintoma', size)
        
            real_medicamento = multiselect(form, 'medicamento', size)

            real_indicador_medicamento = multiselect(form, 'indicador_medicamento', size)

            real_dose_medicamento = multiselect(form, 'dose_medicamento', size)


            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            for i in range(size):
                if real_doenca_cronica[i] is None: continue

                if real_data_primeiro_sintoma[i] is None:
                    data_sintomas = None
                else:
                    data_sintomas = datetime.strptime(real_data_primeiro_sintoma[i], '%d/%m/%Y').date() \
                    if len(real_data_primeiro_sintoma[i]) != 0 \
                    else None

                builder.inserirDoencaCronica(
                    real_doenca_cronica[i], real_medicamento[i], real_indicador_medicamento[i],
                    real_dose_medicamento[i], data_sintomas)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


        # ============== ESF ==============

        has_estrategia_saude_familiar = data_or_null(form['has_estrategia_saude_familiar'], int)

        print('has_estrategia_saude_familiar: {}'.format(has_estrategia_saude_familiar))

        if has_estrategia_saude_familiar == 1:  # Sim
            raw_estrategias_saude_familiar = form['estrategia_saude_familiar'].split(',')

            real_estrategia_saude_familiar = get_real_data(raw_estrategias_saude_familiar)

            print('real_estrategia_saude_familiar: {}'.format(real_estrategia_saude_familiar))

            others_estrategia_saude_familiar = get_others_data(raw_estrategias_saude_familiar)

            print('others_estrategia_saude_familiar: {}'.format(others_estrategia_saude_familiar))

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            for esf in real_estrategia_saude_familiar:
                builder.inserirEstrategiaSaudeFamiliar(esf)
                # others_estrategia_saude_familiar)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

        # ============== Domic??lio e Aux??lios ==============

        qnt_comodos = data_or_null(form['qnt_comodos'], int)

        print('qnt_comodos: {}'.format(qnt_comodos))

        has_agua_encanada = data_or_null(form['has_agua_encanada'], int)

        print('has_agua_encanada: {}'.format(has_agua_encanada))

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        builder.inserirAtendimentoInicial(endereco, qnt_comodos, has_agua_encanada)
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

        has_auxilio = data_or_null(form['has_auxilio'], int)

        if has_auxilio == 1:  # Sim
            raw_auxilios = form['auxilio'].split(',')

            real_auxilios = get_real_data(raw_auxilios)

            print('real_auxilios: {}'.format(real_auxilios))

            others_auxilios = get_others_data(raw_auxilios)

            print('others_auxilios: {}'.format(others_auxilios))

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            for auxilio in real_auxilios:
                builder.inserirBeneficioSocial(auxilio)  # , others_auxilios)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

        # ============== Isolamento domiciliar ==============

        mora_sozinho = data_or_null(form['mora_sozinho'], int)

        print('mora_sozinho: {}'.format(mora_sozinho))

        if mora_sozinho == 2:  # N??o
            size_parentescos = data_or_null(form['mora_sozinho_len'], int)

            parentescos = multiselect(form, 'parentesco_residente_mesma_casa', size_parentescos)

            print('parentescos: {}'.format(parentescos))

            #Parentesco Doen??a Cronica
            size_doencas = data_or_null(form['has_parentesco_doenca_cronica_len'], int)

            parentesco = multiselect(form, 'parentesco', size_doencas)

            print('parentesco: {}'.format(parentesco))

            parentesco_doenca_cronica = multiselect(form, 'parentesco_doenca_cronica', size_doencas)

            print('parentesco_doenca_cronica: {}'.format(parentesco_doenca_cronica))

            parentesco_data_primeiro_sintoma = multiselect(form, 'parentesco_data_primeiro_sintoma', size_doencas)

            print('parentesco_data_primeiro_sintoma: {}'.format(parentesco_data_primeiro_sintoma))

            parentesco_doenca_cronica_medicamento = multiselect(form, 'parentesco_doenca_cronica_medicamento', size_doencas)

            print('parentesco_doenca_cronica_medicamento: {}'.format(parentesco_doenca_cronica_medicamento))

            parentesco_doenca_cronica_medicamento_indicador = multiselect(form, 'parentesco_doenca_cronica_medicamento_indicador', size_doencas)

            print('parentesco_doenca_cronica_medicamento_indicador: {}'.format(parentesco_doenca_cronica_medicamento_indicador))

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            for i in range(size_doencas):
                if parentesco[i] is None: continue

                if parentesco_data_primeiro_sintoma[i] is None:
                    data = None
                else:
                    data = datetime.strptime(parentesco_data_primeiro_sintoma[i], '%d/%m/%Y').date() \
                        if len(parentesco_data_primeiro_sintoma[i]) != 0 \
                        else None

                builder.inserirParentesco(
                    id_parentesco = parentesco[i], id_doenca_cronica = parentesco_doenca_cronica[i],
                    data_sintomas = data,
                    medicamento = parentesco_doenca_cronica_medicamento[i],
                    id_indicador =  parentesco_doenca_cronica_medicamento_indicador[i])
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

            #Parentesco Sintomas
            size_sintomas = data_or_null(form['parentesco_has_sintoma_len'], int)

            parentesco_apresentou_sintoma = multiselect(form, 'parentesco_apresentou_sintoma', size_sintomas)

            print('parentesco_apresentou_sintoma: {}'.format(parentesco_apresentou_sintoma))

            parentesco_sintoma = multiselect(form, 'parentesco_sintoma', size_sintomas)

            print('parentesco_sintoma: {}'.format(parentesco_sintoma))

            parentesco_sintoma_medicamento = multiselect(form, 'parentesco_sintoma_medicamento', size_sintomas)

            print('parentesco_sintoma_medicamento: {}'.format(parentesco_sintoma_medicamento))

            parentesco_quem_indicou_medicamento = multiselect(form, 'parentesco_quem_indicou_medicamento', size_sintomas)

            print('parentesco_quem_indicou_medicamento: {}'.format(parentesco_quem_indicou_medicamento))

            parentesco_dosagem = multiselect(form, 'parentesco_dosagem', size_sintomas)

            print('parentesco_dosagem: {}'.format(parentesco_dosagem))

            is_gravida = multiselect(form, 'is_gravida', size_sintomas)

            print('is_gravida: {}'.format(is_gravida))

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            for i in range(size_sintomas):
                if parentesco_apresentou_sintoma[i] is None: continue
                builder.inserirParentesco(
                    id_parentesco = parentesco_apresentou_sintoma[i], is_mulher_gravida = is_gravida[i],
                    id_sintoma = parentesco_sintoma[i], medicamento = parentesco_sintoma_medicamento[i],
                    id_indicador = parentesco_quem_indicou_medicamento[i], dosagem = parentesco_dosagem[i])
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Aqui sao inseridos apenas os parentescos inseridos que n??o possuem doen??as
            # cr??nicas nem sintomas
            for p in [item for item in parentescos if item not in parentesco and item not in parentesco_apresentou_sintoma]:
                if p is None: continue
                builder.inserirParentesco(id_parentesco = p)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

        # ============== Visitas ==============

        recebeu_visita = data_or_null(form['recebeu_visita'], int)

        print('recebeu_visita: {}'.format(recebeu_visita))

        if recebeu_visita == 1:  # Sim
            size = data_or_null(form['recebeu_visita_len'], int)

            visitas = multiselect(form, 'visita', size)

            print('visitas: {}'.format(visitas))

            pqs_visita = multiselect(form, 'pq_visita', size)

            print('pqs_visita: {}'.format(pqs_visita))

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            for visita, motivo in zip(visitas, pqs_visita):
                if visita is None and motivo is None: continue
                builder.inserirVisita(visita, motivo)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

        # ============== Isolamento domiciliar ==============

        cuidado_sair_casa = data_or_null(form['cuidado_sair_casa'])

        print('cuidado_sair_casa: {}'.format(cuidado_sair_casa))

        has_isolamento = data_or_null(form['has_isolamento'], int)

        print('has_isolamento: {}'.format(has_isolamento))

        if has_isolamento == 1:  # Sim
            isolamento = data_or_null(form['isolamento'])

            print('isolamento: {}'.format(isolamento))

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            builder.inserirIsolamento(True, isolamento, cuidado_sair_casa)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

        elif has_isolamento == 2:  # N??o
            nao_isolamento = data_or_null(form['nao_isolamento'])

            print('nao_isolamento: {}'.format(nao_isolamento))

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            builder.inserirIsolamento(False, nao_isolamento, cuidado_sair_casa)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

        mantem_quarentena = data_or_null(form['mantem_quarentena'], int)

        print('mantem_quarentena: {}'.format(mantem_quarentena))

        if mantem_quarentena == 1:  # Sim
            dias_quarentena = data_or_null(form['dias_quarentena'], int)

            print('dias_quarentena: {}'.format(dias_quarentena))

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            builder.inserirManterEmCasa(True, dias_quarentena)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

        elif mantem_quarentena == 2:  # N??o
            raw_motivo_sair = form['motivo_sair'].split(',')

            real_motivo_sair = get_real_data(raw_motivo_sair)

            print('real_motivo_sair: {}'.format(real_motivo_sair))

            others_motivo_sair = get_others_data(raw_motivo_sair)

            print('others_motivo_sair: {}'.format(others_motivo_sair))

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            builder.inserirManterEmCasa(False)

            for motivo in real_motivo_sair:
                builder.inserirMotivoSair(motivo)  # , others_motivo_sair)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #



        # ============== Sintomas COVID ==============

        has_sintomas = data_or_null(form['has_sintoma'], int)

        print('has_sintomas: {}'.format(has_sintomas))

        if has_sintomas == 1:  # Sim

            size = data_or_null(form['has_sintoma_len'], int)

            real_sintomas = multiselect(form, 'apresentou_sintoma', size)
            
            real_sintoma_medicamento = multiselect(form, 'sintoma_medicamento', size)

            real_quem_indicou_medicamento = multiselect(form, 'quem_indicou_medicamento', size)

            real_dosagem = multiselect(form, 'dosagem', size)


            for i in range(size):
                if real_sintomas[i] is None: continue
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
                builder.inserirSintoma(real_sintomas[i], real_sintoma_medicamento[i],
                                        real_quem_indicou_medicamento[i], real_dosagem[i])
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

        # ============== Orienta????es Finais ==============

        orientacao_final = format_real_data(form['orientacao_final'])

        print(orientacao_final)

        anotacao_orientacoes = data_or_null(form['anotar_orientacoes_finais'])

        print(anotacao_orientacoes)

        builder.inserirOrientacaoFinal(orientacao_final, anotacao_orientacoes)


    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    builder.finalizarPersistencia(id_admsaude, id_paciente)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #



