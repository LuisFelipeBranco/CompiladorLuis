from os import system
import sys

palavrasReservadas = [[1, "main"], [2, "if"], [3, "else"], [4, "while"], [5, "do"], [6, "for"], [7, "int"], [8, "float"], [9, "char"], [10, "id"]]
operadoresAritmeticos = [[11, "+"], [12, "-"], [13, "*"], [14, "/"], [15, "="]]
operadoresRelacionais = [[16, ">"], [17, "<"], [18, ">="], [19, "<="], [20, "=="], [21, "!="]]
tipos = [[22, "valorInt"], [23, "ValorFloat"], [24, "ValorChar"]]
caracteresEspeciais = [[25, "("], [26, ")"], [27, "{"], [28, "}"], [29, ","], [30, ";"], [31, "EOF"]]

linha = 1
coluna = 0
lexema = " "
lido = " "

class Token:
    num = 0
    lex = " "

    def token(self, num, lex):
        self.num = num
        self.lex = lex

    def get_opr(self):
        return self.num

    def get_lex(self):
        return self.lex

class Tabel():

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):#empilha
        self.items.append(item)

    def pop(self):#desempilha
        return self.items.pop()

    def size(self):
        return len(self.items)

def leitura():
    global coluna, linha, lido
    lido = archive.read(1)
    if lido == '\n':
        linha = linha + 1
        coluna = 0

    elif lido == '\t':
        coluna = coluna + 4

    else:
        coluna = coluna + 1

def acumulador():
    global lexema
    lexema = lexema + lido

def Scanner():
    global lexema, lido, caracteresEspeciais, tipos, operadoresRelacionais, operadoresAritmeticos, palavrasReservadas

    while lido:
        lexema = ""

        while lido == '\n' or lido == ' ' or lido == '\t':
            leitura()

        if lido.isdigit():#lendo int e floats
            lexema = lexema + lido
            leitura()

            while lido.isdigit():
                lexema = lexema + lido
                leitura()

            if lido.isalpha():
                lexema = lexema + lido
                print("ERRO: Valor inteiro mal formado! Linha: " + str(linha) + " Coluna: " + str(coluna) + " Ultimo Token lido: " + lexema)
                sys.exit()

            if lido == ".": #numero FLOAT
                lexema = lexema + lido
                leitura()
                if lido == '' or lido == '.' or lido == ',' or lido == ';' or lido.isalpha() or lido == ' ' or lido == '\n' or lido == '\t':
                    print("ERRO: Valor float mal formado! Linha: " + str(linha) + " Coluna: " + str(coluna) + " Ultimo Token lido: " + lexema)
                    sys.exit()

                while lido.isdigit():
                    lexema = lexema + lido
                    leitura()
                if lido == '' or lido == '.' or lido == ',' or lido.isalpha() or lido == ' ':
                    lexema = lexema + lido
                    print("ERRO: Valor float mal formado! Linha: " + str(linha) + " Coluna: " + str(coluna) + " Ultimo Token lido: " + lexema)
                    sys.exit()
                return tok.token(tipos[1][0], lexema) #Valor float

            return tok.token(tipos[0][0], lexema) #Valor INT

        elif lido == "+":
            lexema = lexema + lido
            leitura()
            return tok.token(operadoresAritmeticos[0][0], operadoresAritmeticos[0][1])

        elif lido == "-":
            lexema = lexema + lido
            leitura()
            if lido.isdigit():
                lexema += lido
                print("ERRO: Compilador não aceita numeros negativos! Linha: " + str(linha) + " Coluna: " + str(coluna) + " Ultimo Token lido: " + lexema)
                sys.exit()
            else:
                return tok.token(operadoresAritmeticos[1][0], operadoresAritmeticos[1][1])

        elif lido == "*":
            lexema = lexema + lido
            leitura()
            return tok.token(operadoresAritmeticos[2][0], operadoresAritmeticos[2][1])

        elif lido == "/": #pode ter comentários;
            lexema = lexema + lido
            leitura()
            if lido == "/": #//comentario
                while lido != '\n':
                    leitura()

            elif lido == "*":#/*
                leitura()
                while lido:
                    leitura()
                    if lido == '':
                        print("ERRO: Fim de arquivo dentro de comentário multilinha. Linha: ", linha, "Coluna: ", coluna)
                        sys.exit()
                        return
                    elif lido == "*":
                        leitura()
                        if lido == "/":
                            leitura()
                            break
            else:
                return tok.token(operadoresAritmeticos[3][0], operadoresAritmeticos[3][1])

        elif lido == "=":
            lexema = lexema + lido
            leitura()
            if lido == "=":# igualdade
                lexema = lexema + lido
                leitura()
                return tok.token(operadoresRelacionais[2][0], operadoresRelacionais[2][1])
                break
            else:
                return tok.token(operadoresAritmeticos[4][0], operadoresAritmeticos[4][1])

        elif lido == ".":
            lexema = lexema + lido
            leitura()
            while lido:
                lexema = lexema + lido
                leitura()
                if not (str.isdigit(lido)):
                    lexema = lexema + lido
                    print("ERRO valor float mal formado! Linha: ",linha , " Coluna: ", coluna, " ultimo token lido:", lexema)
                    sys.exit()
                return tok.token(tipos[1][0], lexema)

        elif lido == ">":
            lexema = lexema + lido
            leitura()
            if lido == "=": #>=
                lexema = lexema + lido
                return tok.token(operadoresRelacionais[2][0], operadoresRelacionais[2][1])
                break
            #apenas >
            return tok.token(operadoresRelacionais[0][0], operadoresRelacionais[0][1])
            break

        elif lido == "<":
            lexema = lexema + lido
            leitura()
            if lido == "=":
                lexema = lexema + lido
                return tok.token(operadoresRelacionais[3][0], operadoresRelacionais[3][1])
                break
            return tok.token(operadoresRelacionais[1][0], operadoresRelacionais[1][1])

        elif lido == "!":
            lexema = lexema + lido
            leitura()
            if lido == "=":
                lexema = lexema + lido
                leitura()
                return tok.token(operadoresRelacionais[5][0], operadoresRelacionais[5][1])
            else:
                print("ERRO: Exclamação '!' não seguida de '='  linha: ", linha, " coluna", coluna)
                sys.exit()

        elif lido == ";":
            lexema = lexema + lido
            leitura()
            return tok.token(caracteresEspeciais[5][0], caracteresEspeciais[5][1])

        elif lido == "(":
            lexema = lexema + lido
            leitura()
            return tok.token(caracteresEspeciais[0][0], caracteresEspeciais[0][1])

        elif lido == ")":
            lexema = lexema + lido
            leitura()
            return tok.token(caracteresEspeciais[1][0], caracteresEspeciais[1][1])

        elif lido == "{":
            lexema = lexema + lido
            leitura()
            return tok.token(caracteresEspeciais[2][0], caracteresEspeciais[2][1])

        elif lido == "}":
            lexema = lexema + lido
            leitura()
            return tok.token(caracteresEspeciais[3][0], caracteresEspeciais[3][1])

        elif lido == ",":
            lexema = lexema + lido
            leitura()
            return tok.token(caracteresEspeciais[4][0], caracteresEspeciais[4][1])

        elif lido == ";":
            lexema = lexema + lido
            leitura()
            return tok.token(caracteresEspeciais[5][0], caracteresEspeciais[5][1])

        elif lido.isalpha() or lido == "_":
            lexema = lexema + lido
            leitura()
            while str.isalpha(lido) or lido == "_" or lido.isdigit():
                lexema = lexema + lido
                leitura()
            if lexema == "main":
                return tok.token(palavrasReservadas[0][0], palavrasReservadas[0][1])

            elif lexema == "if":
                return tok.token(palavrasReservadas[1][0], palavrasReservadas[1][1])

            elif lexema == "else":
                return tok.token(palavrasReservadas[2][0], palavrasReservadas[2][1])

            elif lexema == "while":
                return tok.token(palavrasReservadas[3][0], palavrasReservadas[3][1])

            elif lexema == "do":
                return tok.token(palavrasReservadas[4][0], palavrasReservadas[4][1])

            elif lexema == "for":
                return tok.token(palavrasReservadas[5][0], palavrasReservadas[5][1])

            elif lexema == "int":
                return tok.token(palavrasReservadas[6][0], palavrasReservadas[6][1])

            elif lexema == "float":
                return tok.token(palavrasReservadas[7][0], palavrasReservadas[7][1])

            elif lexema == "char":
                return tok.token(palavrasReservadas[8][0], palavrasReservadas[8][1])

            else:

                return tok.token(palavrasReservadas[9][0], palavrasReservadas[9][1])
                #sys.exit()

        elif lido == "":
            return tok.token(caracteresEspeciais[6][0], caracteresEspeciais[6][1])

        elif lido == "'":
            lexema += lido
            leitura()
            if lido.isalpha():#'A
                lexema += lido
                leitura()
                if lido == "'":#'A'
                    leitura()
                    return tok.token(tipos[2][0], tipos[2][1])
                else:#'A;
                    lexema += lido
                    print("ERRO valor char mal formado! Linha: ",linha , " Coluna: ", coluna, " Ultimo token lido:", lexema)
                    sys.exit()
            elif lido.isdigit():#'1
                lexema += lido
                leitura()
                if lido == "'":#'1'
                    leitura()
                    return tok.token(tipos[2][0], tipos[2][1])
                else:
                    print("ERRO valor char mal formado! Linha: ",linha , " Coluna: ", coluna, " Ultimo token lido:", lexema)
                    sys.exit()
            else:
                lexema += lido
                print("ERRO valor char mal formadoB! Linha: ", linha, " Coluna: ", coluna, " Ultimo token lido:", lexema)
                sys.exit()

        else:
            lexema += lido
            print("ERRO: caracter inválido!! Linha: " + str(linha) + ", Coluna: " + str(coluna) + ". Ultimo Token lido: " + lexema)
            sys.exit()

        leitura()

def program():
    Scanner()
    if tok.get_lex() == palavrasReservadas[6][1]:#int
        Scanner()
        if tok.get_lex() == palavrasReservadas[0][1]:#main
            Scanner()
            if tok.get_lex() == caracteresEspeciais[0][1]:#(
                Scanner()
                if tok.get_lex() == caracteresEspeciais[1][1]:#)
                    Scanner()
                    block()
                else:
                    print('ERRO: Má inicialização do programa faltou fecha parentese, Linha: ', linha, ' Coluna: ', coluna)
                    sys.exit()
            else:
                print('ERRO: Má inicialização do programa faltou abre parentese, Linha: ', linha, ' Coluna: ', coluna)
                sys.exit()
        else:
            print('ERRO: Má inicialização do programa faltou o main, Linha: ', linha, ' Coluna: ', coluna)
            sys.exit()
    else:
        print('ERRO: Má inicialização do programa faltou o int, Linha: ', linha, ' Coluna: ', coluna)
        sys.exit()

def block(): #<bloco>::=“{“ {<decl_var>}* {<comando>}* “}”
    if tok.get_lex() == caracteresEspeciais[2][1]:#{
        Scanner()
        while tok.get_lex() != caracteresEspeciais[3][1]:
            var_declaration()#tem ou não
            command()#tem ou não
        if tok.get_lex() == caracteresEspeciais[3][1]:#}
            return
        else:
            print('ERRO: linha: ', linha, ' coluna: ', coluna, ', faltou o [ } ]')
            sys.exit()
    else:#pode ter variavel ou não
        print('ERRO: linha: ', linha, ' coluna: ', coluna, ', problema na inicialização do bloco.')
        sys.exit()

def var_declaration():#<decl_var> ::= <tipo> <id> {,<id>}* ";" olhar o contador de linhas e colunas depois
    if tok.get_lex() == palavrasReservadas[6][1] or tok.get_lex() == palavrasReservadas[7][1] or tok.get_lex() == palavrasReservadas[8][1]:#int/float/char
        if tok.get_lex() == palavrasReservadas[6][1]:#int
            type = 'int'
        if tok.get_lex() == palavrasReservadas[7][1]:#float
            type = 'float'
        if tok.get_lex() == palavrasReservadas[8][1]:#char
            type = 'char'
        Scanner()

        if tok.get_lex() == palavrasReservadas[9][1]:#<type><id>
            sid.push(lexema)
            stype.push(type)
            Scanner()
            if tok.get_lex() == caracteresEspeciais[5][1]:#<type><id><;> declaracao de 1 variavel
                Scanner()
                exit()

            elif tok.get_lex() == caracteresEspeciais[4][1]:#<type><id><,>
                Scanner()
                while tok.get_lex() != caracteresEspeciais[5][1]:
                    if tok.get_lex() == palavrasReservadas[9][1]:#<type><id><,><id>
                        sid.push(lexema)
                        stype.push(type)
                        Scanner()
                        if tok.get_lex() == caracteresEspeciais[4][1]:#<type><id><,><id><,>
                            Scanner()

                        elif tok.get_lex() == caracteresEspeciais[5][1]:#<type><id><,><id><;>
                            Scanner()
                            exit()

                        else:
                            print('ERRO: linha: ', linha, ' coluna: ', coluna, ', declaração de variavel mal feita!')
                            sys.exit()

                    else:
                        print('ERRO: linha: ', linha, ' coluna: ', coluna, ', má declaração de variaveis!')
                        sys.exit()

                print('ERRO: linha: ', linha, ' coluna: ', coluna, ', [;] após a [,]')
                sys.exit()

            else:
                print('ERRO: linha: ', linha, ' coluna: ', coluna, ' declaração de variavel feita de forma incorreta, faltou o [;]')
                sys.exit()

        else:
            print('ERRO linha: ', linha, ' coluna: ', coluna, ', variavel não declarada!', lexema)
            sys.exit()

def iteration():#<iteração>::=while "("<expr_relacional>")" <comando> | do <comando> while "("<expr_relacional>")"";"
    Scanner()
    if tok.get_lex() == palavrasReservadas[3][1]:#while
        Scanner()
        if tok.get_lex() == caracteresEspeciais[0][1]:#<(>
            Scanner()
            relational_expression()
            Scanner()
            if tok.get_lex() == caracteresEspeciais[1][1]:#<)>
                Scanner()
                command()
            else:
                print('ERRO linha: ', linha, ' coluna: ', coluna, ', faltou o <)> do while.')
                sys.exit()
        else:
            print('ERRO linha: ', linha, ' coluna: ', coluna, ', faltou o <(> do while.')
            sys.exit()

    elif tok.get_lex() == palavrasReservadas[4][1]:#do
        Scanner()
        command()
        Scanner()
        if tok.get_lex() == palavrasReservadas[3][1]:#while
            Scanner()
            if tok.get_lex() == caracteresEspeciais[0][1]:#<(>
                Scanner()
                relational_expression()
                Scanner()
                if tok.get_lex() == caracteresEspeciais[1][1]:#<)>
                    Scanner()
                    if tok.get_lex() == caracteresEspeciais[5][1]:#<;>
                        Scanner()
                    else:
                        print('ERRO linha: ', linha, ' coluna: ', coluna, ', faltou o <;> do while.')
                        sys.exit()
                else:
                    print('ERRO linha: ', linha, ' coluna: ', coluna, ', faltou o <)> do while.')
                    sys.exit()
            else:
                print('ERRO linha: ', linha, ' coluna: ', coluna, ', faltou o <)> do while.')
                sys.exit()
        else:
            print('ERRO linha: ', linha, ' coluna: ', coluna, ', faltou comando while')
            sys.exit()

    else:
        print('ERRO linha: ', linha, ' coluna: ', coluna, ', comando fora do laço de iteração!')
        sys.exit()

def relational_expression():#<expr_relacional>::=<expr_arit> <op_relacional> <expr_arit>
    pass

def command():#<comando> ::= <comando_básico> | <iteração> | if "("<expr_relacional>")" <comando> {else <comando>}?
    if tok.get_lex() == palavrasReservadas[9][1] or tok.get_lex() == caracteresEspeciais[2][0]:#<id> ou <{>
        basic_command()
    elif tok.get_lex() == palavrasReservadas[5][1] or tok.get_lex() == palavrasReservadas[6][1]:#<do> ou <while>
        iteration()
    elif tok.get_lex() == palavrasReservadas[1][1]:#if
        Scanner()
        if tok.get_lex() == caracteresEspeciais[0][1]:#<(>
            Scanner()
            relational_expression()
            Scanner()
            if tok.get_lex() == caracteresEspeciais[1][1]:#<)>
                Scanner()
                command()
                Scanner()
                if tok.get_lex() == caracteresEspeciais[2][1]:#{
                    Scanner()
                    if tok.get_lex() == palavrasReservadas[2][1]:#else
                        Scanner()
                        command()
                        Scanner()
                        if tok.get_lex() == caracteresEspeciais[3][1]:#}
                            Scanner()
                        else:
                            print('ERRO: linha: ', linha, 'coluna: ', coluna, ', esperado <}>.')
                            sys.exit()
                    else:
                        print('ERRO: linha: ', linha, 'coluna: ', coluna, ', esperado comando <else>.')
                        sys.exit()
                else:
                    Scanner()
            else:
                print('ERRO: linha: ', linha, 'coluna: ', coluna, ', faltou o <)> do comando <if>')
                sys.exit()
        else:
            print('ERRO: linha: ', linha, 'coluna: ', coluna, ', expressão relacional do comando <if> não declarada!')
            sys.exit()

def arithmetic_expression():#<expr_arit>::=<expr_arit> "+" <termo>   | <expr_arit> "-" <termo> | <termo>
    Scanner()

def attribution():#<atribuição>::=<id> "=" <expr_arit> ";"
    Scanner()
    if tok.get_lex() == palavrasReservadas[9][1]:#<id>
        Scanner()
        if tok.get_lex() == operadoresAritmeticos[4][1]:#<=>
            Scanner()
            arithmetic_expression()
            Scanner()
            if tok.get_lex() == caracteresEspeciais[5][1]:#<;>
                exit()
            else:
                print('ERRO: linha: ', linha, 'coluna: ', coluna, ', e esperado um <;>!')
                sys.exit()
        else:
            print('ERRO: linha: ', linha, 'coluna: ', coluna, ', na atribuição e esperado um <=> após a variavel!')
            sys.exit()
    else:
        print('ERRO: linha: ', linha, 'coluna: ', coluna, ', é esperado uma variável!')
        sys.exit()

def basic_command():#<comando_básico>::=<atribuição> | <bloco>
    Scanner()
    if tok.get_lex() == palavrasReservadas[9][1]:#<id>
        attribution()
    elif tok.get_lex() == caracteresEspeciais[2][1]:#<{>
        block()
    else:
        print('ERRO: linha: ', linha, ' coluna: ', coluna, ' má formação de comando básico!')
        sys.exit()

def term():#<termo>::=<termo> "*" <fator> | <termo> “/” <fator> | <fator>
    pass

def factor():#<fator>::=“(“ <expr_arit> “)” | <id> | <float> | <inteiro> | <char>
    if tok.get_lex() == caracteresEspeciais[0][1]:#<(>
        Scanner()
        arithmetic_expression()
        Scanner()
        if tok.get_lex() == caracteresEspeciais[1][1]:#<)>
            pass

    elif tok.get_opr() == tipos[0][0] or tok.get_opr() == tipos[0][1] or tok.get_opr() == tipos[0][2] or tok.get_lex() == palavrasReservadas[9][1]:
        return

    else:
        print('ERRO: linha: ', linha, 'coluna: ', coluna, ', erro na formação do fator.')
        sys.exit()

if __name__ == "__main__":
    arch = sys.argv[1]
    archive = open(arch, "r")
    tok = Token()
    sid = Tabel()
    stype = Tabel()

    program()

    '''while(lido != ''):
        Scanner()
        print('____________________________________________')
        print("Classificação do Token: ", tok.get_opr())
        print("Lexema do Token: ", tok.get_lex())
        print('linha: ', linha)
        print('coluna: ', coluna)
        print('____________________________________________')'''


    archive.closed