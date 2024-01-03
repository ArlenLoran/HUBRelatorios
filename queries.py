import oracledb
import cryptography.hazmat.primitives.kdf.pbkdf2

def QueryReceiving(datestart, dateend, sku, lote, client, cod):
    connection = oracledb.connect(user="RBC01PRD_RO", password="rbc012023roDlx09prd",
                                  dsn="USMEGAP004-SCAN.PHX-DC.DHL.COM:1521/RBC01PRD")

    cursor = connection.cursor()
    cursor.execute(f"""
                    SELECT *
            FROM 
                (SELECT ia.invact_id,
                     ia.invnum,
                     am.adrnam,
                     t.carcod,
                     TO_CHAR(ia.trndte,
                     'DD/MM/YYYY HH24:MI:SS') trndte, lotnum, ia.prtnum, ia.prt_client_id, ia.supnum, ia.trknum, ia.wh_id, ia.rcvqty qty
                FROM adrmst am, invact ia, supmst sm, rcvtrk rt, trlr t
                WHERE ia.supnum = sm.supnum(+)
                        AND ia.client_id = sm.client_id(+)
                        AND sm.adr_id = am.adr_id(+)
                        AND ia.trknum = rt.trknum(+)
                        AND ia.wh_id = rt.wh_id(+)
                        AND rt.trlr_id = t.trlr_id(+)
                        AND ia.actcod = 'INVRCV'
                        AND ia.trndte >= to_date('{datestart}', 'DD/MM/YYYY')
                        AND ia.trndte <= to_date('{dateend}', 'DD/MM/YYYY')+1
                        AND ia.wh_id IN ('{cod}')
                        AND ia.client_id IN ('{client}')
                        AND ia.lotnum = nvl('{lote}', ia.lotnum)
                        AND ia.prtnum = '{sku}' 
                -- and am.locale_id = 'US_ENGLISH'

                UNION
                SELECT ia.invact_id,
                     ia.invnum,
                     am.adrnam,
                     t.carcod carcod,
                     TO_CHAR(ia.trndte,
                     'DD/MM/YYYY HH24:MI:SS') trndte, lotnum, ia.prtnum, ia.prt_client_id, ia.supnum, ia.trknum, ia.wh_id, ia.rcvqty qty
                FROM adrmst am, arc_invact ia, supmst sm, 
                    (SELECT DISTINCT trknum,
                     wh_id,
                     trlr_id
                    FROM arc_rcvtrk) rt, 
                        (SELECT DISTINCT trlr_id,
                     carcod
                        FROM arc_trlr) t
                        WHERE ia.supnum = sm.supnum(+)
                                AND ia.client_id = sm.client_id(+)
                                AND sm.adr_id = am.adr_id(+)
                                AND ia.trknum = rt.trknum(+)
                                AND ia.wh_id = rt.wh_id(+)
                                AND rt.trlr_id = t.trlr_id(+)
                                AND ia.actcod = 'INVRCV'
                                AND ia.trndte >= to_date('{datestart}', 'DD/MM/YYYY')
                                AND ia.trndte <= to_date('{dateend}', 'DD/MM/YYYY')+1
                                AND ia.wh_id IN ('{cod}')
                                AND ia.client_id IN ('{client}')
                                AND ia.lotnum = nvl('{lote}', ia.lotnum)
                                AND ia.prtnum = '{sku}' 
                        -- and am.locale_id = 'US_ENGLISH'

                        ORDER BY  trndte )
                    WHERE ROWNUM < 30001 """,
                   )


    result = cursor.fetchall()
    return result

def QueryShipment(datestart, dateend, sku, lote, client, cod):
    connection = oracledb.connect(user="RBC01PRD_RO", password="rbc012023roDlx09prd",
                                  dsn="USMEGAP004-SCAN.PHX-DC.DHL.COM:1521/RBC01PRD")

    cursor = connection.cursor()
    cursor.execute(f"""SELECT *
FROM 
    (SELECT o.wh_id,
         to_char(decode(cd.cartyp,
         'S', mf.shpdte, 'L', s.loddte, 'T', s.loddte, nvl(mf.shpdte, s.loddte) ), 'DD/MM/YYYY HH24:MI') dte, id.lotnum, o.ordnum, id.prtnum, id.prt_client_id, s.ship_id, sum(id.untqty) qty, am.adrcty, am.adrnam, am.adrpsz, am.adrstc
    FROM ord o, adrmst am, invdtl id, ord_line ol, shipment s, shipment_line sl, cardtl cd, 
        (SELECT ship_id,
         min(shpdte) shpdte
        FROM manfst mf
        GROUP BY  ship_id) mf
        WHERE ol.client_id = sl.client_id
                AND ol.ordnum = sl.ordnum
                AND ol.ordlin = sl.ordlin
                AND ol.ordsln = sl.ordsln
                AND ol.wh_id = sl.wh_id
                AND o.st_adr_id = am.adr_id
                AND o.client_id = ol.client_id
                AND o.ordnum = ol.ordnum
                AND o.wh_id = ol.wh_id
                AND s.ship_id = sl.ship_id
                AND s.wh_id = sl.wh_id
                AND sl.ship_line_id = id.ship_line_id
                AND s.carcod = cd.carcod(+)
                AND s.srvlvl = cd.srvlvl(+)
                AND s.ship_id = mf.ship_id(+)
                AND o.wh_id IN ('{cod}')
                AND id.prt_client_id IN ('{client}')
                AND decode(cd.cartyp, 'S', mf.shpdte, 'L', s.loddte, 'T', s.loddte, nvl(mf.shpdte, s.loddte) ) >= to_date('{datestart}', 'DD/MM/YYYY')
                AND decode(cd.cartyp, 'S', mf.shpdte, 'L', s.loddte, 'T', s.loddte, nvl(mf.shpdte, s.loddte) ) <= to_date('{dateend}', 'DD/MM/YYYY')+1
                AND id.prtnum = '{sku}'
                AND id.lotnum = nvl('{lote}', id.lotnum) 
        -- and am.locale_id = 'AR_SPANISH'
        
        GROUP BY  o.wh_id, decode(cd.cartyp, 'S', mf.shpdte, 'L', s.loddte, 'T', s.loddte, nvl(mf.shpdte, s.loddte) ), id.lotnum, o.ordnum, id.prtnum, id.prt_client_id, s.ship_id, am.adrcty, am.adrnam, am.adrpsz, am.adrstc
        UNION
        SELECT o.wh_id,
         to_char(decode(cd.cartyp,
         'S', mf.shpdte, 'L', s.loddte, 'T', s.loddte, nvl(mf.shpdte, s.loddte) ), 'DD/MM/YYYY HH24:MI') dte, id.lotnum, o.ordnum, id.prtnum, id.prt_client_id, s.ship_id, sum(id.untqty) qty, am.adrcty, am.adrnam, am.adrpsz, am.adrstc
        FROM arc_ord o, adrmst am, arc_invdtl id, arc_ord_line ol, arc_shipment s, arc_shipment_line sl, cardtl cd, 
            (SELECT ship_id,
         min(shpdte) shpdte
            FROM arc_manfst mf
            GROUP BY  ship_id) mf
            WHERE ol.client_id = sl.client_id
                    AND ol.ordnum = sl.ordnum
                    AND ol.ordlin = sl.ordlin
                    AND ol.ordsln = sl.ordsln
                    AND ol.wh_id = sl.wh_id
                    AND o.st_adr_id = am.adr_id
                    AND o.client_id = ol.client_id
                    AND o.ordnum = ol.ordnum
                    AND o.wh_id = ol.wh_id
                    AND s.ship_id = sl.ship_id
                    AND s.wh_id = sl.wh_id
                    AND sl.ship_line_id = id.ship_line_id
                    AND s.carcod = cd.carcod(+)
                    AND s.srvlvl = cd.srvlvl(+)
                    AND s.ship_id = mf.ship_id(+)
                    AND o.wh_id IN ('{cod}')
                    AND id.prt_client_id IN ('{client}')
                    AND decode(cd.cartyp, 'S', mf.shpdte, 'L', s.loddte, 'T', s.loddte, nvl(mf.shpdte, s.loddte) ) >= to_date('{datestart}', 'DD/MM/YYYY')
                    AND decode(cd.cartyp, 'S', mf.shpdte, 'L', s.loddte, 'T', s.loddte, nvl(mf.shpdte, s.loddte) ) <= to_date('{dateend}', 'DD/MM/YYYY')+1
                    AND id.prtnum = '{sku}'
                    AND id.lotnum = nvl('{lote}', id.lotnum) 
            -- and am.locale_id = 'AR_SPANISH'
            
            GROUP BY  o.wh_id, decode(cd.cartyp, 'S', mf.shpdte, 'L', s.loddte, 'T', s.loddte, nvl(mf.shpdte, s.loddte) ), id.lotnum, o.ordnum, id.prtnum, id.prt_client_id, s.ship_id, am.adrcty, am.adrnam, am.adrpsz, am.adrstc
            ORDER BY  dte ASC )
        WHERE ROWNUM < 30001""",
                   )


    result = cursor.fetchall()
    return result


def QueryStock(sku, lote, client, cod):
    connection = oracledb.connect(user="RBC01PRD_RO", password="rbc012023roDlx09prd",
                                  dsn="USMEGAP004-SCAN.PHX-DC.DHL.COM:1521/RBC01PRD")

    cursor = connection.cursor()
    cursor.execute(f"""SELECT 
 TO_CHAR(iv.lstdte, 'DD/MM/YYYY') AS DATA,
    (SELECT lngdsc
    FROM dscmst
    WHERE colnam LIKE 'arecod|wh_id'
            AND colval = 
        (SELECT arecod
        FROM locmst
        WHERE iv.stoloc = locmst.stoloc
                AND locmst.wh_id = '{cod}') || '|{cod}'
                AND locale_id = 'BR_PORTUGUESE' AND LNGDSC NOT LIKE 'Ajustes de Cycle Count' AND LNGDSC NOT LIKE 'Adjustments' AND LNGDSC IS NOT NULL) AS AREA, iv.stoloc AS LOCAL, iv.lodnum AS LPN, iv.prtnum AS PRODUTO, 
        (SELECT lngdsc
        FROM prtdsc
        WHERE colval = iv.prtnum || '|{client}|{cod}' AND iv.prtnum = '{sku}' AND iv.lotnum IN nvl(('{lote}'), iv.lotnum)
                AND locale_id = 'BR_PORTUGUESE') AS DESCRICAO, 
        (SELECT lngdsc
        FROM dscmst
        WHERE colnam = 'invsts'
                AND colval = iv.invsts
                AND locale_id = 'BR_PORTUGUESE') AS STATUS, iv.lotnum AS LOTE, iv.untqty AS UNIDADES, TO_CHAR(iv.rcvdte, 'DD/MM/YYYY') AS RECEBIMENTO, TO_CHAR(iv.mandte, 'DD/MM/YYYY') AS MA, TO_CHAR(iv.expire_dte, 'DD/MM/YYYY') AS EXPIRACAO, TRUNC(iv.expire_dte) - TRUNC(SYSDATE) AS DIAS,   IV.AGE_PFLNAM 
    FROM inventory_view iv
    WHERE prt_client_id = '{client}' AND iv.prtnum = '{sku}' AND iv.lotnum IN nvl(('{lote}'), iv.lotnum)
        AND stoloc NOT LIKE 'TRL%'""",
                   )

    result = cursor.fetchall()
    return result

def QueryProducao(datestart, dateend):
    connection = oracledb.connect(user="PROT2PRD_RO", password="Prot2RO2023Pr0thprd",
                                  dsn="USMEGAP004-SCAN.PHX-DC.DHL.COM:1521/PROTPRD2_RPT")

    cursor = connection.cursor()
    cursor.execute(f"""SELECT TO_DATE(D2_EMISSAO, 'yyyymmdd'), SUBSTR(D2_DOC,5,5), D2_COD, D2_QUANT, D2_QTSEGUM, D2_SEGUM FROM SD2100
WHERE D2_FILIAL = '156PKG015642' AND D2_TES IN ('5F2','5F3') and TO_DATE(D2_EMISSAO, 'yyyy/mm/dd') BETWEEN TO_DATE('{datestart}', 'dd/mm/yyyy') AND TO_DATE('{dateend}', 'dd/mm/yyyy') AND r_e_c_d_e_l_ = 0""",
                   )

    result = cursor.fetchall()
    return result

def QueryDevolucao(datestart, dateend):
    connection = oracledb.connect(user="PROT2PRD_RO", password="Prot2RO2023Pr0thprd",
                                  dsn="USMEGAP004-SCAN.PHX-DC.DHL.COM:1521/PROTPRD2_RPT")

    cursor = connection.cursor()
    cursor.execute(f"""SELECT TO_DATE(D2_EMISSAO, 'yyyymmdd'), SUBSTR(D2_DOC,5,5), D2_COD, D2_QUANT, D2_QTSEGUM, D2_SEGUM FROM SD2100 
WHERE D2_FILIAL = '156PKG015642' AND D2_TES IN ('5F4') and TO_DATE(D2_EMISSAO, 'yyyy/mm/dd') BETWEEN TO_DATE('{datestart}', 'dd/mm/yyyy') AND  TO_DATE('{dateend}', 'dd/mm/yyyy') AND r_e_c_d_e_l_ = 0""",
                   )

    result = cursor.fetchall()
    return result

def QueryAnalitico():
    connection = oracledb.connect(user="PROT2PRD_RO", password="Prot2RO2023Pr0thprd",
                                  dsn="USMEGAP004-SCAN.PHX-DC.DHL.COM:1521/PROTPRD2_RPT")

    cursor = connection.cursor()
    cursor.execute(f"""SELECT 
                    --an.b2_vatu1 "Valor Estoque",
                     
                    --an.b2_cm1 "Custo Unitário",
                     TRIM(an.b2_cod) "Produto", TRIM(pr.b1_desc) "Descrição", pr.b1_segum "Unidade de Medida", pr.b1_conv "Unidades por caixa", b2_qtsegum "Caixas", an.b2_qatu "Estoque Disponível"
                    FROM sb2100 an
                    LEFT JOIN sb1100 pr
                        ON pr.b1_cod = an.b2_cod
                            AND pr.b1_filial = an.b2_filial
                            AND pr.b1_segum IN ('EA' , 'MT' , 'CA' , 'GM' )
                    WHERE b2_filial = '156PKG015642' 
                    --AND an.b2_qfim <> 0
                     
                    --and TRIM(an.b2_cod) = '3219560'
                            AND an.b2_qatu <> 0
                    ORDER BY  1 
                    --an.b2_qfim, 5 desc""",
                   )

    result = cursor.fetchall()
    return result

def QueryOcupation(cod):
    connection = oracledb.connect(user="RBC01PRD_RO", password="rbc012023roDlx09prd",
                                  dsn="USMEGAP004-SCAN.PHX-DC.DHL.COM:1521/RBC01PRD")

    cursor = connection.cursor()
    cursor.execute(f"""SELECT COUNT(stoloc) "Capacidade",
         SUM(CASE
    WHEN useflg = 1
        AND stoflg = 1
        AND locsts IN ('E')
        AND pndqvl = 0 THEN
    1
    ELSE 0
    END ) "Disponiveis" , SUM(CASE
    WHEN (stoflg = 0
        OR useflg = 0)
        AND NOT ( locsts NOT IN ('E')
        OR pndqvl <> 0 ) THEN
    1
    ELSE 0 END) "Bloqueadas", SUM(CASE
    WHEN NOT( stoflg = 0
        OR useflg = 0 )
        AND (locsts NOT IN ('E')
        OR pndqvl <> 0 ) THEN
    1
    ELSE 0 END) "Ocupadas" , SUM(CASE
    WHEN (stoflg = 0
        OR useflg = 0)
        AND ( locsts NOT IN ('E')
        OR pndqvl <> 0 ) THEN
    1
    ELSE 0 END) "Ocup Bloq", arecod AS "Area" , LOCHGT AS "Altura Local", DSC1.LNGDSC "Velzon", DSC2.LNGDSC "Abccod", to_char(sysdate, 'dd/mm/yyyy hh24:mi:ss') data
FROM locmst lc
LEFT JOIN dscmst DSC1
    ON DSC1.colnam IN ('velzon')
        AND DSC1.locale_id = 'BR_PORTUGUESE'
        AND DSC1.COLVAL = velzon
LEFT JOIN dscmst DSC2
    ON DSC2.colnam IN ( 'abccod')
        AND DSC2.locale_id = 'BR_PORTUGUESE'
        AND DSC2.COLVAL = abccod
WHERE wh_id = '{cod}'
        AND arecod NOT IN ('ADJS', 'YARD', 'EXPR', 'CADJ', 'SADJ', 'AVAGES', 'RCKT', 'BLOQ', 'SSTG', 'RSTG', 'RDTS000001', 'WRKS', 'SHIP', 'RDTS', 'DCK') 
--AND to_char(sysdate, 'hh24') in ('13','22')
GROUP BY  arecod, lochgt, velzon, 
--, USEFLG, STOFLG, LOCSTS, pndqvl
 dsc1.lngdsc, DSC2.LNGDSC""",
                   )


    result = cursor.fetchall()
    return result

def QueryBaseDlx(cod, client):
    connection = oracledb.connect(user="RBC01PRD_RO", password="rbc012023roDlx09prd",
                                  dsn="USMEGAP004-SCAN.PHX-DC.DHL.COM:1521/RBC01PRD")

    cursor = connection.cursor()
    cursor.execute(f"""--SELECT SUM("Caixas") termino, sum_over inicio FROM(
SELECT
    TO_CHAR(  MIN(iv.ADDDTE), 'DD/MM/YYYY') AS "Dt. Inclus",
    dsc_lc.lngdsc AS "Area",
    iv.stoloc AS "Local Armazenagem",
    iv.lodnum AS "Num. LPN",
    --iv.subnum AS "Identificador Peca",
    iv.prtnum AS "Cod. Produto",
    dsc_pt.lngdsc AS "Descricao",
    pr.prtfam "Familia",
    CASE
    WHEN embl.prtnum IS NOT NULL /*OR pr.PRTFAM = 'PACKING'*/ THEN 'Packing'
    WHEN pr.PRTFAM IN ('CORRELATOS', 'COSMETICOS', 'Health') THEN 'Health'
    ELSE 'Hygiene' END as "Categoria",
    dsc_sts.lngdsc AS "Status Inventario",
    iv.lotnum AS "Número Lote",
    SUM(iv.untqty) AS "Caixas",
    to_char(NVL(MIN(iv.RCVDTE), MIN(iv.ADDDTE) ), 'DD/MM/YYYY')  AS "Data Receb",
    TO_CHAR(MIN(iv.mandte), 'DD/MM/YYYY') AS "Data de Ma",
    TO_CHAR(MIN(dly.trndte), 'DD/MM/YYYY') AS "Alter. Status",
    TO_CHAR(MIN(iv.expire_dte), 'DD/MM/YYYY') AS "Data de Ex",
    IV.AGE_PFLNAM "Perfil Envelhecimento",
    TRUNC(MIN(iv.expire_dte)) - TRUNC(SYSDATE) AS "Dias Expir",
    CASE
        WHEN SUM(iv.untqty) /pr_d.ppd  < 0.5 THEN '<50%'
        WHEN SUM(iv.untqty) /pr_d.ppd >= 0.5 AND SUM(iv.untqty) /pr_d.ppd <0.7 THEN '50% > x < 70%'
        WHEN SUM(iv.untqty) /pr_d.ppd >= 0.7 AND SUM(iv.untqty) /pr_d.ppd <1 THEN '70% > x < Full'
        ELSE 'Full'
    END "Fracionamento",
    TRUNC(sysdate - COALESCE(MIN(dly.trndte), MIN(iv.RCVDTE), MIN(iv.ADDDTE), MIN(iv.mandte) )) "Residence Time", --sum_over,
    CASE
        WHEN iv.invsts = 'A' THEN 0
        WHEN TRUNC(sysdate - COALESCE(MIN(dly.trndte), MIN(iv.RCVDTE), MIN(iv.ADDDTE), MIN(iv.mandte) )) <= 5 THEN  1 
        WHEN TRUNC(sysdate - COALESCE(MIN(dly.trndte), MIN(iv.RCVDTE), MIN(iv.ADDDTE), MIN(iv.mandte) )) <= 15 THEN  2 
        WHEN TRUNC(sysdate - COALESCE(MIN(dly.trndte), MIN(iv.RCVDTE), MIN(iv.ADDDTE), MIN(iv.mandte) )) <= 50 THEN 3 
        WHEN TRUNC(sysdate - COALESCE(MIN(dly.trndte), MIN(iv.RCVDTE), MIN(iv.ADDDTE), MIN(iv.mandte) )) <= 100 THEN  4 
        ELSE 5 END "Criticidade" 
FROM
    (SELECT
        iv.adddte,
        --dsc_lc.lngdsc ,
        iv.stoloc ,
        iv.lodnum ,
        iv.subnum ,
        iv.prtnum ,
        --dsc_pt.lngdsc ,
        --pr.prtfam ,
        invsts,
        iv.lotnum ,
        iv.untqty,
        NVL(iv.rcvdte,iv.adddte ) rcvdte ,
        iv.mandte,
        iv.expire_dte,
        IV.AGE_PFLNAM,
        lc.arecod,
        SUM(untqty) over() sum_over
    FROM
        inventory_view iv
    LEFT JOIN
        locmst lc ON lc.wh_id = '{cod}' AND iv.stoloc = lc.stoloc
    WHERE
        iv.prt_client_id = '{client}'
        AND lc.arecod NOT IN ('SHIP', 'ADJS', 'CADJ')) iv
LEFT JOIN
    dscmst dsc_lc
    ON dsc_lc.colval = iv.arecod || '|{cod}' AND dsc_lc.locale_id = 'US_ENGLISH' AND dsc_lc.colnam = 'arecod|wh_id'
LEFT JOIN
    prtdsc dsc_pt	ON	dsc_pt.locale_id = 'US_ENGLISH' AND dsc_pt.colval = iv.prtnum || '|{client}|{cod}'
LEFT JOIN
    dscmst dsc_sts	ON	dsc_sts.colnam = 'invsts' AND dsc_sts.colval = iv.invsts AND dsc_sts.locale_id = 'US_ENGLISH'
LEFT JOIN
    (select
        pr_d.prtnum,
        MAX(CASE WHEN pr_d.uomcod = 'PA' THEN pr_d.untqty END) PPD
    from 
        prtftp_dtl pr_d
    WHERE  pr_d.wh_id = '{cod}'
    GROUP BY
        pr_d.prtnum) pr_d ON pr_d.prtnum = iv.prtnum
LEFT JOIN
    prtmst pr ON pr.prtnum = iv.prtnum AND pr.wh_id_tmpl = '{cod}'
LEFT JOIN
    (SELECT  iv.prtnum 
    FROM
        inventory_view iv
    WHERE
        iv.prt_client_id = '{client}'
        AND iv.lst_arecod NOT IN ('SHIP', 'ADJS', 'CADJ')
    HAVING
        COUNT( CASE WHEN INSTR( iv.lotnum, 'DHL') >0 THEN iv.prtnum END) > 0
    GROUP BY
        iv.prtnum) embl ON embl.prtnum = pr.prtnum
LEFT JOIN
    (SELECT
        MAX(dly.trndte) trndte,
        LISTAGG(CASE WHEN lin = 1 THEN dly.actcod END, '') WITHIN GROUP (ORDER BY dly.actcod) actcod,
        dly.subnum,
        dly.prtnum,
        dly.toinvs
    FROM
        (SELECT
            dly.*,
            ROW_NUMBER() OVER ( PARTITION BY dly.subnum, dly.prtnum, dly.toinvs ORDER BY dly.trndte DESC) lin 
        FROM   
            (SELECT dly.trndte,
                    dly.actcod,
                    --NVL(dly.lodnum,sub.lodnum) lodnum,
                    dly.subnum,
                    dly.prtnum,
                    --dly.lotnum,
                    --dsc.lngdsc reacod,
                    --dly.frinvs,
                    dly.toinvs
            FROM dlytrn dly
            LEFT JOIN invsub sub
                ON sub.subnum = dly.subnum
            LEFT JOIN
                dscmst dsc
                ON colnam = 'reacod' AND locale_id = 'BR_PORTUGUESE' AND colval = dly.reacod
            WHERE dly.wh_id = '{cod}' 
                --AND dly.subnum IS NULL
                AND dly.frinvs <> dly.toinvs) dly) dly
    GROUP BY
        dly.subnum,
        dly.prtnum,
        dly.toinvs) dly ON dly.subnum = iv.subnum  AND
                            dly.prtnum = iv.prtnum  AND
                            dly.toinvs = iv.invsts
GROUP BY
    dsc_lc.lngdsc ,
    iv.stoloc ,
    iv.lodnum ,
    sum_over,
    --iv.subnum ,
    iv.prtnum ,
    dsc_pt.lngdsc ,
    pr.prtfam ,
    iv.invsts,
    dsc_sts.lngdsc,
     embl.prtnum,
    dsc_pt.lngdsc,
    iv.lotnum ,
    IV.AGE_PFLNAM,
    pr_d.ppd --) GROUP BY sum_over""",
                   )


    result = cursor.fetchall()
    return result

def QueryAlteracaoLote(lote):
    connection = oracledb.connect(user="RBC01PRD_RO", password="rbc012023roDlx09prd",
                                  dsn="USMEGAP004-SCAN.PHX-DC.DHL.COM:1521/RBC01PRD")

    cursor = connection.cursor()
    cursor.execute(f"""select TRNDTE DATA,
     LODNUM LPN,
     PRTNUM SKU,
     TRNQTY QTD,
     PRT_CLIENT_ID CLIENTE,
     FR_VALUE DE,
     TO_VALUE PARA,
     ins_user_id USUARIO
 from DLYTRN where actcod = 'INVATTCHG' AND prtnum = '21010' and lotnum IN nvl(('{lote}'), lotnum)""",
                   )

    result = cursor.fetchall()
    print(result)
    return result







