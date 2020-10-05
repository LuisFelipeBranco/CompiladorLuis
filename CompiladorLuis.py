from os import system
import sys
#palavraReservadas = [["main", 1], ["tipo_float", 2], ["tipo_int", 3], ["tipo_char", 4], ["while", 5], ["do", 6], ["if", 7], ["else", 8], ["id", 9]]
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

        while lido == '\n' or lido == ' ':
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
                lexema = lexema + lido
                #print("Erro na linha: ", linha, "Coluna: ", coluna)
                return tok.token(palavrasReservadas[9][0], palavrasReservadas[9][1])
                sys.exit()

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

if __name__ == "__main__":
    arch = sys.argv[1]
    archive = open(arch, "r")
    tok = Token()

    while(lido != ''):
        Scanner()
        print('____________________________________________')
        print("Classificação do Token: ", tok.get_opr())
        print("Lexema do Token: ", tok.get_lex())
        print('____________________________________________')


    archive.closed