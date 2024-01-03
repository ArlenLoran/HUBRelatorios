from controls import return_control_reference
from flet import *
from queries import *
import pandas as pd
import openpyxl
import os
import psutil

control_map = return_control_reference()

def closeapp(e):
    PROCNAME = "EXCEL.EXE"
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()

def open_file(e, name):
    os.startfile(name)


def close_banner(e):
    e.page.banner.open = False
    e.page.update()

def open_banner_error(mensa, e):
    e.page.banner = Banner(
        bgcolor="red",
        leading=Icon(icons.ERROR_OUTLINE_ROUNDED, color="white", size=30),
        content=Text(
            mensa, color="white"
        ),
        actions=[
            TextButton("OK", on_click=close_banner, style=ButtonStyle(color="white"))
        ]
    )
    e.page.banner.open = True
    e.page.update()


def RecevingToExcel(e):
    closeapp(e)
    for key, value in control_map.items():
        if key == 'CardReceiving':
            operacao = value.controls[0].content.controls[6].content.controls[1].value
            sku = value.controls[0].content.controls[7].content.controls[1].value
            lote = value.controls[0].content.controls[8].content.controls[1].value
            datainicial = value.controls[0].content.controls[9].content.controls[1].value
            datafinal = value.controls[0].content.controls[10].content.controls[1].value
            if operacao == None:
                open_banner_error("Selecione a operação!", e)
            elif sku == "":
                open_banner_error("Digite o SKU!", e)
            elif datainicial == "":
                open_banner_error("Digite a data inicial!", e)
            elif datafinal == "":
                open_banner_error("Digite a data final!", e)
            else:
                value.controls[0].shadow = BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=colors.with_opacity(1, "orange"),
                    offset=Offset(2, 2)
                ),
                value.controls[0].update()
                value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                value.controls[0].content.controls[4].controls[1].value = "Rodando query"
                value.controls[0].width = 160
                value.controls[0].height = 180
                value.controls[0].disabled = True
                value.controls[0].update()
                if operacao == "Itupeva":
                    cliente = "RBCCID"
                    cod = "RCKT"
                elif operacao == "Embu":
                    cliente = "CID02"
                    cod = "WH02"
                try:
                    result = QueryReceiving(datainicial, datafinal, sku, lote, cliente, cod)
                    value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                    value.controls[0].content.controls[4].controls[1].value = "Gerando arquivo"
                    value.controls[0].update()
                    keys = ['id', 'nf', 'local', 'transp', 'recebimento', 'lote', 'sku', 'cliente', 'no', 'placa',
                            'cod', 'pager']
                    if not result == []:
                        result = [dict(zip(keys, values)) for values in result]
                        data = {'INVACT_ID': [], 'INVNUM': [], 'ADRNAM': [], 'CARCOD': [], 'TRNDTE': [], 'LOTNUM': [],
                                'PRTNUM': [], 'PRT_CLIENT_ID': [], 'SUPNUM': [], 'TRKNUM': [], 'WH_ID': [], 'QTY': []}
                        for x in result:
                            data['INVACT_ID'].append(x['id']),
                            data['INVNUM'].append(x['nf']),
                            data['ADRNAM'].append(x['local']),
                            data['CARCOD'].append(x['transp']),
                            data['TRNDTE'].append(x['recebimento']),
                            data['LOTNUM'].append(x['lote']),
                            data['PRTNUM'].append(x['sku']),
                            data['PRT_CLIENT_ID'].append(x['cliente']),
                            data['SUPNUM'].append(x['no']),
                            data['TRKNUM'].append(x['placa']),
                            data['WH_ID'].append(x['cod']),
                            data['QTY'].append(x['pager']),
                        df = pd.DataFrame(data)
                        df.to_excel("RelatorioRecebimento.xlsx", index=False)
                        value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                        value.controls[0].content.controls[4].controls[1].value = "Abrindo excel"
                        value.controls[0].update()
                        open_file(e, 'RelatorioRecebimento.xlsx')
                        value.controls[0].disabled = False
                        value.controls[0].update()
                        value.controls[0].content.controls[4].controls[0].bgcolor = "cyan"
                        value.controls[0].content.controls[4].controls[1].value = "Gerar relatório"
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                        value.controls[0].update()
                    else:
                        open_banner_error("Não há resultados para essa busca!", e)
                        value.controls[0].content.controls[4].controls[0].bgcolor = "cyan"
                        value.controls[0].content.controls[4].controls[1].value = "Gerar relatório"
                        value.controls[0].disabled = False
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                        value.controls[0].update()
                except:
                    open_banner_error("Houve um erro ao rodar a query, verifique se está conectado em uma rede DHL!", e)
                    value.controls[0].content.controls[4].controls[0].bgcolor = "red"
                    value.controls[0].content.controls[4].controls[1].value = "Erro de conexão"
                    value.controls[0].disabled = False
                    value.controls[0].shadow = BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=colors.with_opacity(0.21, "black"),
                        offset=Offset(2, 2)
                    ),
                    value.controls[0].update()

def ShipmentToExcel(e):
    closeapp(e)
    for key, value in control_map.items():
        if key == 'CardShipment':
            operacao = value.controls[0].content.controls[6].content.controls[1].value
            sku = value.controls[0].content.controls[7].content.controls[1].value
            lote = value.controls[0].content.controls[8].content.controls[1].value
            datainicial = value.controls[0].content.controls[9].content.controls[1].value
            datafinal = value.controls[0].content.controls[10].content.controls[1].value
            if operacao == None:
                open_banner_error("Selecione a operação!", e)
            elif sku == "":
                open_banner_error("Digite o SKU!", e)
            elif datainicial == "":
                open_banner_error("Digite a data inicial!", e)
            elif datafinal == "":
                open_banner_error("Digite a data final!", e)
            else:
                value.controls[0].shadow = BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=colors.with_opacity(1, "orange"),
                    offset=Offset(2, 2)
                ),
                value.controls[0].update()
                value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                value.controls[0].content.controls[4].controls[1].value = "Rodando query"
                value.controls[0].width = 160
                value.controls[0].height = 180
                value.controls[0].disabled = True
                value.controls[0].update()
                if operacao == "Itupeva":
                    cliente = "RBCCID"
                    cod = "RCKT"
                elif operacao == "Embu":
                    cliente = "CID02"
                    cod = "WH02"
                try:
                    result = QueryShipment(datainicial, datafinal, sku, lote, cliente, cod)
                    value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                    value.controls[0].content.controls[4].controls[1].value = "Gerando arquivo"
                    value.controls[0].update()
                    keys = ['wh_id', 'dte', 'lotnum', 'ordnum', 'prtnum', 'prt_client_id', 'ship_id', 'qty', 'adrcty', 'adrnam',
                            'adrpsz', 'adrstc']
                    if not result == []:
                        result = [dict(zip(keys, values)) for values in result]
                        data = {'WH_ID': [], 'DTE': [], 'LOTNUM': [], 'ORDNUM': [], 'PRTNUM': [], 'PRT_CLIENT_ID': [],
                                'SHIP_ID': [], 'QTY': [], 'ADRCTY': [], 'ADRNAM': [], 'ADRPSZ': [], 'ADRSTC': []}
                        for x in result:
                            data['WH_ID'].append(x['wh_id']),
                            data['DTE'].append(x['dte']),
                            data['LOTNUM'].append(x['lotnum']),
                            data['ORDNUM'].append(x['ordnum']),
                            data['PRTNUM'].append(x['prtnum']),
                            data['PRT_CLIENT_ID'].append(x['prt_client_id']),
                            data['SHIP_ID'].append(x['ship_id']),
                            data['QTY'].append(x['qty']),
                            data['ADRCTY'].append(x['adrcty']),
                            data['ADRNAM'].append(x['adrnam']),
                            data['ADRPSZ'].append(x['adrpsz']),
                            data['ADRSTC'].append(x['adrstc']),
                        df = pd.DataFrame(data)
                        df.to_excel("RelatorioExpedicao.xlsx", index=False)
                        value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                        value.controls[0].content.controls[4].controls[1].value = "Abrindo excel"
                        value.controls[0].update()
                        open_file(e, 'RelatorioExpedicao.xlsx')
                        value.controls[0].disabled = False
                        value.controls[0].update()
                        value.controls[0].content.controls[4].controls[0].bgcolor = "cyan"
                        value.controls[0].content.controls[4].controls[1].value = "Gerar relatório"
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                        value.controls[0].update()
                    else:
                        open_banner_error("Não há resultados para essa busca!", e)
                        value.controls[0].content.controls[4].controls[0].bgcolor = "cyan"
                        value.controls[0].content.controls[4].controls[1].value = "Gerar relatório"
                        value.controls[0].disabled = False
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                        value.controls[0].update()
                except:
                    open_banner_error("Houve um erro ao rodar a query, verifique se está conectado em uma rede DHL!", e)
                    value.controls[0].content.controls[4].controls[0].bgcolor = "red"
                    value.controls[0].content.controls[4].controls[1].value = "Erro de conexão"
                    value.controls[0].disabled = False
                    value.controls[0].shadow = BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=colors.with_opacity(0.21, "black"),
                        offset=Offset(2, 2)
                    ),
                    value.controls[0].update()

def StockToExcel(e):
    closeapp(e)
    for key, value in control_map.items():
        if key == 'CardStock':
            operacao = value.controls[0].content.controls[6].content.controls[1].value
            sku = value.controls[0].content.controls[7].content.controls[1].value
            lote = value.controls[0].content.controls[8].content.controls[1].value
            if operacao == None:
                open_banner_error("Selecione a operação!", e)
            elif sku == "":
                open_banner_error("Digite o SKU!", e)
            else:
                value.controls[0].shadow = BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=colors.with_opacity(1, "orange"),
                    offset=Offset(2, 2)
                ),
                value.controls[0].update()
                value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                value.controls[0].content.controls[4].controls[1].value = "Rodando query"
                value.controls[0].width = 160
                value.controls[0].height = 180
                value.controls[0].disabled = True
                value.controls[0].update()
                if operacao == "Itupeva":
                    cliente = "RBCCID"
                    cod = "RCKT"
                elif operacao == "Embu":
                    cliente = "CID02"
                    cod = "WH02"
                try:
                    result = QueryStock(sku, lote, cliente, cod)
                    value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                    value.controls[0].content.controls[4].controls[1].value = "Gerando arquivo"
                    value.controls[0].update()
                    keys = ['data', 'area', 'local', 'lpn', 'produto', 'descricao', 'status', 'lote', 'unidades', 'recebimento',
                            'manufatura', 'expiracao', 'dias', 'age']
                    if not result == []:
                        result = [dict(zip(keys, values)) for values in result]
                        data = {'DATA': [], 'AREA': [], 'LOCAL': [], 'LPN': [], 'PRODUTO': [], 'DESCRICAO': [],
                                'STATUS': [], 'LOTE': [], 'UNIDADES': [], 'RECEBIMENTO': [], 'MANUFATURA': [], 'EXPIRACAO': [], 'DIAS': [], 'AGE': []}
                        for x in result:
                            data['DATA'].append(x['data']),
                            data['AREA'].append(x['area']),
                            data['LOCAL'].append(x['local']),
                            data['LPN'].append(x['lpn']),
                            data['PRODUTO'].append(x['produto']),
                            data['DESCRICAO'].append(x['descricao']),
                            data['STATUS'].append(x['status']),
                            data['LOTE'].append(x['lote']),
                            data['UNIDADES'].append(x['unidades']),
                            data['RECEBIMENTO'].append(x['recebimento']),
                            data['MANUFATURA'].append(x['manufatura']),
                            data['EXPIRACAO'].append(x['expiracao']),
                            data['DIAS'].append(x['dias']),
                            data['AGE'].append(x['age']),
                        df = pd.DataFrame(data)
                        df.to_excel("RelatorioEstoque.xlsx", index=False)
                        value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                        value.controls[0].content.controls[4].controls[1].value = "Abrindo excel"
                        value.controls[0].update()
                        open_file(e, 'RelatorioEstoque.xlsx')
                        value.controls[0].disabled = False
                        value.controls[0].update()
                        value.controls[0].content.controls[4].controls[0].bgcolor = "cyan"
                        value.controls[0].content.controls[4].controls[1].value = "Gerar relatório"
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                        value.controls[0].update()
                    else:
                        open_banner_error("Não há resultados para essa busca!", e)
                        value.controls[0].content.controls[4].controls[0].bgcolor = "cyan"
                        value.controls[0].content.controls[4].controls[1].value = "Gerar relatório"
                        value.controls[0].disabled = False
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                        value.controls[0].update()
                except:
                    open_banner_error("Houve um erro ao rodar a query, verifique se está conectado em uma rede DHL!", e)
                    value.controls[0].content.controls[4].controls[0].bgcolor = "red"
                    value.controls[0].content.controls[4].controls[1].value = "Erro de conexão"
                    value.controls[0].disabled = False
                    value.controls[0].shadow = BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=colors.with_opacity(0.21, "black"),
                        offset=Offset(2, 2)
                    ),
                    value.controls[0].update()

def ProdutionToExcel(e):
    closeapp(e)
    for key, value in control_map.items():
        if key == 'CardProduction':
            datainicial = value.controls[0].content.controls[6].content.controls[1].value
            datafinal = value.controls[0].content.controls[7].content.controls[1].value
            if datainicial == "":
                open_banner_error("Digite a data inicial!", e)
            elif datafinal == "":
                open_banner_error("Digite a data final!", e)
            else:
                value.controls[0].shadow = BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=colors.with_opacity(1, "orange"),
                    offset=Offset(2, 2)
                ),
                value.controls[0].update()
                value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                value.controls[0].content.controls[4].controls[1].value = "Rodando query"
                value.controls[0].width = 160
                value.controls[0].height = 180
                value.controls[0].disabled = True
                value.controls[0].update()
                try:
                    result = QueryProducao(datainicial, datafinal)
                    value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                    value.controls[0].content.controls[4].controls[1].value = "Gerando arquivo"
                    value.controls[0].update()
                    keys = ['data', 'nota', 'oferta', 'unidade', 'quantidade', 'um']
                    if not result == []:
                        result = [dict(zip(keys, values)) for values in result]
                        data = {'DATA': [], 'NOTA': [], 'OFERTA': [], 'UNIDADE': [], 'QUANTIDADE': [], 'UM': []}
                        for x in result:
                            data['DATA'].append(x['data']),
                            data['NOTA'].append(x['nota']),
                            data['OFERTA'].append(x['oferta']),
                            data['UNIDADE'].append(x['unidade']),
                            data['QUANTIDADE'].append(x['quantidade']),
                            data['UM'].append(x['um']),
                        df = pd.DataFrame(data)
                        df.to_excel("RelatorioProducao.xlsx", index=False)
                        value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                        value.controls[0].content.controls[4].controls[1].value = "Abrindo excel"
                        value.controls[0].update()
                        open_file(e, 'RelatorioProducao.xlsx')
                        value.controls[0].disabled = False
                        value.controls[0].update()
                        value.controls[0].content.controls[4].controls[0].bgcolor = "cyan"
                        value.controls[0].content.controls[4].controls[1].value = "Gerar relatório"
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                        value.controls[0].update()
                    else:
                        open_banner_error("Não há resultados para essa busca!", e)
                        value.controls[0].content.controls[4].controls[0].bgcolor = "cyan"
                        value.controls[0].content.controls[4].controls[1].value = "Gerar relatório"
                        value.controls[0].disabled = False
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                        value.controls[0].update()
                except:
                    open_banner_error("Houve um erro ao rodar a query, verifique se está conectado em uma rede DHL!", e)
                    value.controls[0].content.controls[4].controls[0].bgcolor = "red"
                    value.controls[0].content.controls[4].controls[1].value = "Erro de conexão"
                    value.controls[0].disabled = False
                    value.controls[0].shadow = BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=colors.with_opacity(0.21, "black"),
                        offset=Offset(2, 2)
                    ),
                    value.controls[0].update()

def DevolutionToExcel(e):
    closeapp(e)
    for key, value in control_map.items():
        if key == 'CardDevolution':
            datainicial = value.controls[0].content.controls[6].content.controls[1].value
            datafinal = value.controls[0].content.controls[7].content.controls[1].value
            if datainicial == "":
                open_banner_error("Digite a data inicial!", e)
            elif datafinal == "":
                open_banner_error("Digite a data final!", e)
            else:
                value.controls[0].shadow = BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=colors.with_opacity(1, "orange"),
                    offset=Offset(2, 2)
                ),
                value.controls[0].update()
                value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                value.controls[0].content.controls[4].controls[1].value = "Rodando query"
                value.controls[0].width = 160
                value.controls[0].height = 180
                value.controls[0].disabled = True
                value.controls[0].update()
                try:
                    result = QueryDevolucao(datainicial, datafinal)
                    value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                    value.controls[0].content.controls[4].controls[1].value = "Gerando arquivo"
                    value.controls[0].update()
                    keys = ['data', 'nota', 'oferta', 'unidade', 'quantidade', 'um']
                    if not result == []:
                        result = [dict(zip(keys, values)) for values in result]
                        data = {'DATA': [], 'NOTA': [], 'OFERTA': [], 'UNIDADE': [], 'QUANTIDADE': [], 'UM': []}
                        for x in result:
                            data['DATA'].append(x['data']),
                            data['NOTA'].append(x['nota']),
                            data['OFERTA'].append(x['oferta']),
                            data['UNIDADE'].append(x['unidade']),
                            data['QUANTIDADE'].append(x['quantidade']),
                            data['UM'].append(x['um']),
                        df = pd.DataFrame(data)
                        df.to_excel("RelatorioDevolucao.xlsx", index=False)
                        value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                        value.controls[0].content.controls[4].controls[1].value = "Abrindo excel"
                        value.controls[0].update()
                        open_file(e, 'RelatorioDevolucao.xlsx')
                        value.controls[0].disabled = False
                        value.controls[0].update()
                        value.controls[0].content.controls[4].controls[0].bgcolor = "cyan"
                        value.controls[0].content.controls[4].controls[1].value = "Gerar relatório"
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                        value.controls[0].update()
                    else:
                        open_banner_error("Não há resultados para essa busca!", e)
                        value.controls[0].content.controls[4].controls[0].bgcolor = "cyan"
                        value.controls[0].content.controls[4].controls[1].value = "Gerar relatório"
                        value.controls[0].disabled = False
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                        value.controls[0].update()
                except:
                    open_banner_error("Houve um erro ao rodar a query, verifique se está conectado em uma rede DHL!", e)
                    value.controls[0].content.controls[4].controls[0].bgcolor = "red"
                    value.controls[0].content.controls[4].controls[1].value = "Erro de conexão"
                    value.controls[0].disabled = False
                    value.controls[0].shadow = BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=colors.with_opacity(0.21, "black"),
                        offset=Offset(2, 2)
                    ),
                    value.controls[0].update()

def AnaliticoToExcel(e):
    closeapp(e)
    for key, value in control_map.items():
        if key == 'CardAnalytic':
            value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
            value.controls[0].content.controls[4].controls[1].value = "Rodando query"
            value.controls[0].width = 160
            value.controls[0].height = 180
            value.controls[0].disabled = True
            value.controls[0].update()
            try:
                value.controls[0].shadow = BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=colors.with_opacity(1, "orange"),
                    offset=Offset(2, 2)
                ),
                value.controls[0].update()
                result = QueryAnalitico()
                value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                value.controls[0].content.controls[4].controls[1].value = "Gerando arquivo"
                value.controls[0].update()
                keys = ['produto', 'descricao', 'um', 'unporcaixa', 'quantidade', 'disponivel']
                if not result == []:
                    result = [dict(zip(keys, values)) for values in result]
                    data = {'PRODUTO': [], 'DESCRICAO': [], 'UM': [], 'UNPORCAIXA': [], 'QUANTIDADE': [], 'DISPONIVEL': []}
                    for x in result:
                        data['PRODUTO'].append(x['produto']),
                        data['DESCRICAO'].append(x['descricao']),
                        data['UM'].append(x['um']),
                        data['UNPORCAIXA'].append(x['unporcaixa']),
                        data['QUANTIDADE'].append(x['quantidade']),
                        data['DISPONIVEL'].append(x['disponivel']),
                    df = pd.DataFrame(data)
                    df.to_excel("RelatorioAnalitico.xlsx", index=False)
                    value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                    value.controls[0].content.controls[4].controls[1].value = "Abrindo excel"
                    value.controls[0].update()
                    open_file(e, 'RelatorioAnalitico.xlsx')
                    value.controls[0].disabled = False
                    value.controls[0].update()
                    value.controls[0].content.controls[4].controls[0].bgcolor = "cyan"
                    value.controls[0].content.controls[4].controls[1].value = "Gerar relatório"
                    value.controls[0].shadow = BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=colors.with_opacity(0.21, "black"),
                        offset=Offset(2, 2)
                    ),
                    value.controls[0].update()
                else:
                    open_banner_error("Não há resultados para essa busca!", e)
                    value.controls[0].content.controls[4].controls[0].bgcolor = "cyan"
                    value.controls[0].content.controls[4].controls[1].value = "Gerar relatório"
                    value.controls[0].disabled = False
                    value.controls[0].shadow = BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=colors.with_opacity(0.21, "black"),
                        offset=Offset(2, 2)
                    ),
                    value.controls[0].update()
            except:
                open_banner_error("Houve um erro ao rodar a query, verifique se está conectado em uma rede DHL!", e)
                value.controls[0].content.controls[4].controls[0].bgcolor = "red"
                value.controls[0].content.controls[4].controls[1].value = "Erro de conexão"
                value.controls[0].disabled = False
                value.controls[0].shadow = BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=colors.with_opacity(0.21, "black"),
                    offset=Offset(2, 2)
                ),
                value.controls[0].update()

def OcupationToExcel(e):
    closeapp(e)
    for key, value in control_map.items():
        if key == 'CardOcupation':
            operacao = value.controls[0].content.controls[6].content.controls[1].value
            if operacao == None:
                open_banner_error("Selecione a operação!", e)
            else:
                if operacao == "Itupeva":
                    cod = "RCKT"
                elif operacao == "Embu":
                    cod = "WH02"
                value.controls[0].shadow = BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=colors.with_opacity(1, "orange"),
                    offset=Offset(2, 2)
                ),
                value.controls[0].update()
                value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                value.controls[0].content.controls[4].controls[1].value = "Rodando query"
                value.controls[0].width = 160
                value.controls[0].height = 180
                value.controls[0].disabled = True
                value.controls[0].update()
                try:
                    result = QueryOcupation(cod)
                    value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                    value.controls[0].content.controls[4].controls[1].value = "Gerando arquivo"
                    value.controls[0].update()
                    keys = ['Capacidade', 'Disponiveis', 'Bloqueadas', 'OcupBloq', 'Area', 'AlturaLocal', 'Velzon', 'Abccod', 'data']
                    if not result == []:
                        result = [dict(zip(keys, values)) for values in result]
                        data = {'CAPACIDADE': [], 'DISPONIVEIS': [], 'BLOQUEADAS': [], 'OCUPBLOQ': [], 'AREA': [], 'ALTURALOCAL': [], 'VELZON': [], 'ABCCOD': [], 'DATA': []}
                        for x in result:
                            data['CAPACIDADE'].append(x['Capacidade']),
                            data['DISPONIVEIS'].append(x['Disponiveis']),
                            data['BLOQUEADAS'].append(x['Bloqueadas']),
                            data['OCUPBLOQ'].append(x['OcupBloq']),
                            data['AREA'].append(x['Area']),
                            data['ALTURALOCAL'].append(x['AlturaLocal']),
                            data['VELZON'].append(x['Velzon']),
                            data['ABCCOD'].append(x['Abccod']),
                            data['DATA'].append(x['data']),
                        df = pd.DataFrame(data)
                        df.to_excel("RelatorioOcupation.xlsx", index=False)
                        value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                        value.controls[0].content.controls[4].controls[1].value = "Abrindo excel"
                        value.controls[0].update()
                        open_file(e, 'RelatorioOcupation.xlsx')
                        value.controls[0].disabled = False
                        value.controls[0].update()
                        value.controls[0].content.controls[4].controls[0].bgcolor = "cyan"
                        value.controls[0].content.controls[4].controls[1].value = "Gerar relatório"
                        value.controls[0].update()
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                        value.controls[0].update()
                    else:
                        open_banner_error("Não há resultados para essa busca!", e)
                        value.controls[0].content.controls[4].controls[0].bgcolor = "cyan"
                        value.controls[0].content.controls[4].controls[1].value = "Gerar relatório"
                        value.controls[0].disabled = False
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                        value.controls[0].update()
                except:
                    open_banner_error("Houve um erro ao rodar a query, verifique se está conectado em uma rede DHL!", e)
                    value.controls[0].content.controls[4].controls[0].bgcolor = "red"
                    value.controls[0].content.controls[4].controls[1].value = "Erro de conexão"
                    value.controls[0].disabled = False
                    value.controls[0].shadow = BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=colors.with_opacity(0.21, "black"),
                        offset=Offset(2, 2)
                    ),
                    value.controls[0].update()

def BaseDlxToExcel(e):
    closeapp(e)
    for key, value in control_map.items():
        if key == 'CardBaseDlx':
            value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
            value.controls[0].content.controls[4].controls[1].value = "Rodando query"
            value.controls[0].width = 160
            value.controls[0].height = 180
            value.controls[0].disabled = True
            value.controls[0].update()
            operacao = value.controls[0].content.controls[6].content.controls[1].value
            if operacao == None:
                open_banner_error("Selecione a operação!", e)
            else:
                if operacao == "Itupeva":
                    client = "RBCCID"
                    cod = "RCKT"
                elif operacao == "Embu":
                    client = "CID02"
                    cod = "WH02"
                value.controls[0].shadow = BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=colors.with_opacity(1, "orange"),
                    offset=Offset(2, 2)
                ),
                value.controls[0].update()
                try:
                    result = QueryBaseDlx(cod, client)
                    value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                    value.controls[0].content.controls[4].controls[1].value = "Gerando arquivo"
                    value.controls[0].update()
                    keys = ['inclusao', 'area', 'local', 'lpn', 'produto', 'descricao', 'familia', 'categoria', 'status', 'lote', 'caixas', 'recebimento', 'manufatura', 'altstatus', 'expedicao', 'age', 'diasexpiracao', 'fracionamento', 'residencetime', 'criticidade']
                    if not result == []:
                        result = [dict(zip(keys, values)) for values in result]
                        data = {'INCLUSAO': [], 'AREA': [], 'LOCAL': [], 'LPN': [], 'PRODUTO': [], 'DESCRICAO': [], 'FAMILIA': [], 'CATEGORIA': [], 'STATUS': [], 'LOTE': [], 'CAIXAS': [], 'RECEBIMENTO': [], 'MANUFATURA': [], 'ALTSTATUS': [], 'EXPEDICAO': [], 'AGE': [], 'DIASEXPIRACAO': [], 'FRACIONAMENTO': [], 'RESIDENCETIME': [], 'CRITICIDADE': []}
                        for x in result:
                            data['INCLUSAO'].append(x['inclusao']),
                            data['AREA'].append(x['area']),
                            data['LOCAL'].append(x['local']),
                            data['LPN'].append(x['lpn']),
                            data['PRODUTO'].append(x['produto']),
                            data['DESCRICAO'].append(x['descricao']),
                            data['FAMILIA'].append(x['familia']),
                            data['CATEGORIA'].append(x['categoria']),
                            data['STATUS'].append(x['status']),
                            data['LOTE'].append(x['lote']),
                            data['CAIXAS'].append(x['caixas']),
                            data['RECEBIMENTO'].append(x['recebimento']),
                            data['MANUFATURA'].append(x['manufatura']),
                            data['ALTSTATUS'].append(x['altstatus']),
                            data['EXPEDICAO'].append(x['expedicao']),
                            data['AGE'].append(x['age']),
                            data['DIASEXPIRACAO'].append(x['diasexpiracao']),
                            data['FRACIONAMENTO'].append(x['fracionamento']),
                            data['RESIDENCETIME'].append(x['residencetime']),
                            data['CRITICIDADE'].append(x['criticidade']),
                        df = pd.DataFrame(data)
                        df.to_excel("BaseDLX.xlsx", index=False)
                        value.controls[0].content.controls[4].controls[0].bgcolor = "orange"
                        value.controls[0].content.controls[4].controls[1].value = "Abrindo excel"
                        value.controls[0].update()
                        open_file(e, 'BaseDLX.xlsx')
                        value.controls[0].disabled = False
                        value.controls[0].update()
                        value.controls[0].content.controls[4].controls[0].bgcolor = "cyan"
                        value.controls[0].content.controls[4].controls[1].value = "Gerar relatório"
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                        value.controls[0].update()
                    else:
                        open_banner_error("Não há resultados para essa busca!", e)
                        value.controls[0].content.controls[4].controls[0].bgcolor = "cyan"
                        value.controls[0].content.controls[4].controls[1].value = "Gerar relatório"
                        value.controls[0].disabled = False
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                        value.controls[0].update()
                except:
                    open_banner_error("Houve um erro ao rodar a query, verifique se está conectado em uma rede DHL!", e)
                    value.controls[0].content.controls[4].controls[0].bgcolor = "red"
                    value.controls[0].content.controls[4].controls[1].value = "Erro de conexão"
                    value.controls[0].disabled = False
                    value.controls[0].shadow = BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=colors.with_opacity(0.21, "black"),
                        offset=Offset(2, 2)
                    ),
                    value.controls[0].update()



