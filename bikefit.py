# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect
from fit import Bikefit
from banco import UsaBanco
from datetime import datetime

def visitas():
	data = datetime.now()
	dia = data.strftime('%Y-%m-%d')
	with UsaBanco() as cursor:
		sql = f"select count(data) from bikefit where data like '{dia}%';"
		cursor.execute(sql)
		qt_calculos = cursor.fetchone()
		return qt_calculos[0]

app = Flask(__name__)


# Chama a pagina principal, o formulario para insercao das informacoes para o calculo #
@app.route('/')
def bikefit():
    return render_template('bikefit.html',
                           dia = visitas(),
                           the_title='bike fit virtual')

# Calcula e exibe a pagina de resultado com as medidas do usuario e para a configuracao da bicicleta #
# O try serve para pegar os valores enviados pelo formulario, trocar a virgula pelo ponto caso o #
# usuario insira usando o padrao nacional para decimais, converter para float e atribuir as variaveis. # 
@app.route('/resultados',methods=['POST'])
def resultado():  
    try:
        cavalo = float(request.form['cavalo'].replace(',','.')) 
        if cavalo < 3:
            cavalo = cavalo * 100
    except:
        cavalo = False
    try:
        esterno = float(request.form['esterno'].replace(',','.'))
        if esterno < 3:
            esterno = esterno * 100
    except:
        esterno = False
    try:
        braco = float(request.form['braco'].replace(',','.'))
        if braco < 3:
            braco = braco * 100
    except:
        braco = False
    
    # Segue se os tres valores forem enviados, puderam ser convertidos para float, e o esterno for maior que os outros dois ou retorna erro.    
    if (cavalo and esterno and braco) and (esterno > cavalo and esterno > braco) and (esterno < 250):
        tronco = esterno - cavalo
        bfit = Bikefit(cavalo, esterno, braco)
        quadroSpeed = bfit.quadro_speed()
        quadroMTB = bfit.quadro_mtb()
        alturaSelim = bfit.altura_selim()
        topTubeEfetivo = bfit.top_tube_efetivo()
        email = request.form['email']
        
        # Insere os dados do usuario e os calculos na tabela bikefit
        with UsaBanco() as cursor:
            sql =   """insert into bikefit(
                email,
                data,
                cavalo,
                esterno,
                braco,
                tronco,
                quadro_speed,
                quadro_mtb,
                altura_selim,
                top_tube_efetivo
            )
                values(
                    %s, now(),%s,%s,%s,%s,%s,%s,%s,%s);"""           
            cursor.execute(sql,(email,cavalo,esterno,braco,tronco,quadroSpeed,quadroMTB,alturaSelim,topTubeEfetivo,))
        
        # Retorna a pagina de resultados do bikefit    
        return render_template( 'resultados.html',
		    dia = visitas(),
            email = email,
            cavalo = cavalo,
            esterno = esterno,
            braco = braco,
            tronco = tronco,
            the_title = "resultados",
            quadroSpeed = quadroSpeed,
            quadroMTB = quadroMTB,
            alturaSelim = alturaSelim,
            topTubeEfetivo = topTubeEfetivo,                            
        )
        
    # Exibe pagina de erro se os dados nao forem corretamente inseridos pelo usuario no formulario
    else:
        return render_template('erro.html',
							   dia = visitas(),
                               the_title="erro")
    
    
# Chama a pagina para o usuario pesquisar por calculos anteriores inserindo o email
@app.route('/buscaranteriores')
def anteriores():
    return render_template('buscaranteriores.html',
						   dia = visitas(),
                           the_title='buscar anteriores')

    
# Chama a pagina com o resultado da busca por calculos anteriores    
@app.route('/resultadosanteriores',methods=['POST'])
def resultadosanteriores():
    email = request.form['email']
    
    # Busca no banco os resultados anteriores na tabela bikefit
    with UsaBanco() as cursor:
        sql = """select data,
                    cavalo,
                    esterno,
                    braco,
                    tronco,
                    quadro_speed,
                    quadro_mtb,
                    altura_selim,
                    top_tube_efetivo 
                    from bikefit where email = %s;"""
        cursor.execute(sql,(email,))
        resultado = cursor.fetchall()
    
    # Mostra a pagina com os resultados anteriores buscados pelo e-mail    
    return render_template('resultadosanteriores.html',
							the_title='calculos anteriores',
							dia = visitas(),
							resultado = resultado)


# Chama a pagina do mural de mensagens
@app.route('/muraldemensagens', methods=['POST','GET'])
def muraldemensagens():
    if(request.form):
        
        if not '<a' in request.form['mensagem']: # Solucao meia boca para evitar spam
            if len(request.form['mensagem']) > 0: # para nao inserir comentarios vazios
                nome = request.form['nome'] 
                email = request.form['email']
                mensagem = request.form['mensagem']
                
                # Insere as mensagens no banco muraldemensagens
                with UsaBanco() as cursor:
                    sql = """insert into muraldemensagens(data,nome,email,mensagem)values(now(),%s,%s,%s)"""
                    cursor.execute(sql,(nome,email,mensagem,))
    
    # Busca as mensagens do mural de mensagens para exibir na pagina                
    with UsaBanco() as cursor:
        sql = """select data,nome,email,mensagem from muraldemensagens order by id desc;"""
        cursor.execute(sql)
        mensagens_mural_de_mensagens = cursor.fetchall()
    
    # Exibe a pagina do mural de mensagens
    return render_template('muraldemensagens.html',
                           the_title="mural de mensagens",
						   dia = visitas(),
                           mensagens = mensagens_mural_de_mensagens,
                           )
   
   
# Chama a pagina de links, a qual futuramente devo usar um banco de dados para cadastra-los
@app.route('/links')
def links():
    return render_template('links.html',
						   dia = visitas(),
                           the_title="links")

# Chama a pagina "sobre" todas as vezes em que o site daria erro 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('sobre.html',
						dia = visitas(),
                        the_title="sobre")

# Chama a pagina "sobre"
@app.route('/sobre')
def sobre():
    return render_template('sobre.html',
						dia = visitas(),
                        the_title='sobre')

@app.route('/aluguel')
def aluguel():
	return redirect("http://www.nograu.com.br:5001/",code=302)

@app.route('/cafe')
def cafe():
    return redirect("http://www.nograu.com.br:5002/",code=302)

@app.route('/appformularios')
def appformularios():
    return redirect("http://www.nograu.com.br:5003/",code=302)


@app.route('/pcd')
def pcd():
    return redirect("http://www.nograu.com.br:5004/",code=302)

# Executa o aplicativo
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
