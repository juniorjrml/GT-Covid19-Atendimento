from .sections import *

fieldsetConjunto1 = {
    "name": "Dados pessoais",
    "sections": [
        informacoesBasicas,
    ],
}

fieldsetConjunto2 = {
    "name": "Dados sobre saúde",
    "sections": [
        condicaoclinica,
        doencasCronicas,
        medicamentos,
        esfReferencia,
    ],
}

fieldsetConjunto3 = {
    "name": "Dados sociais",
    "sections": [
        caracteristicasDomicilioAuxilio,
    ],
}

fieldsetConjunto4 = {
    "name": "Isolamento domiciliar",
    "sections": [
        domicilio,
        visitas,
        isolamentoDomiciliar,
    ],
}

fieldsetConjunto5 = {
    "name": "Sintomas COVID",
    "sections": [
        sintomascovid,
    ],
}

fieldsetConjunto6 = {
    "name": "Encerramento",
    "sections": [
        orientacoesfinais
    ],
}
