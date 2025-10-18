import os
import sys

def _escrever_subrotinas_correcao(f_out, estado):
    # Cheguei no limite da fita de Sipser e acessei um branco antes dela (#)
    f_out.write(f"corr_esq_{estado} 0 _ R sub_shift0_{estado}\n")
    f_out.write(f"corr_esq_{estado} 1 _ R sub_shift1_{estado}\n")
    f_out.write(f"corr_esq_{estado} _ _ R sub_shiftB_{estado}\n")
    f_out.write(f"corr_esq_{estado} & _ R sub_shiftF_{estado}\n")
    
    # Shift Right de zeros
    f_out.write(f"\nsub_shift0_{estado} 0 0 R sub_shift0_{estado}\n")
    f_out.write(f"sub_shift0_{estado} 1 0 R sub_shift1_{estado}\n")
    f_out.write(f"sub_shift0_{estado} _ 0 R sub_shiftB_{estado}\n")
    f_out.write(f"sub_shift0_{estado} & 0 R sub_shiftF_{estado}\n")
    
    # Shift Right de uns
    f_out.write(f"\nsub_shift1_{estado} 0 1 R sub_shift0_{estado}\n")
    f_out.write(f"sub_shift1_{estado} 1 1 R sub_shift1_{estado}\n")
    f_out.write(f"sub_shift1_{estado} _ 1 R sub_shiftB_{estado}\n")
    f_out.write(f"sub_shift1_{estado} & 1 R sub_shiftF_{estado}\n")
    
    # Shift Right de _
    f_out.write(f"\nsub_shiftB_{estado} 0 _ R sub_shift0_{estado}\n")
    f_out.write(f"sub_shiftB_{estado} 1 _ R sub_shift1_{estado}\n")
    f_out.write(f"sub_shiftB_{estado} _ _ R sub_shiftB_{estado}\n")
    f_out.write(f"sub_shiftB_{estado} & _ R sub_shiftF_{estado}\n")
    
    # Shift Right de F (&)
    f_out.write(f"\nsub_shiftF_{estado} _ & L sub_retorna_{estado}\n")
    
    # Corrigir o cabeçote, voltando para o início
    f_out.write(f"\nsub_retorna_{estado} _ _ L sub_retorna_{estado}\n")
    f_out.write(f"sub_retorna_{estado} 0 0 L sub_retorna_{estado}\n")
    f_out.write(f"sub_retorna_{estado} 1 1 L sub_retorna_{estado}\n")
    f_out.write(f"sub_retorna_{estado} # # R {estado}_sip\n")
    
    # Correção da fita à direita (quando encontra &)
    f_out.write(f"\ncorr_dir_{estado} _ & L {estado}_sip\n\n")

def converter_para_infinita(f_out, linhas):
    f_out.write("0 0 # R desloca_dir_0\n")
    f_out.write("0 1 # R desloca_dir_1\n")
    f_out.write("0 _ # R 0_inf\n\n")
    f_out.write("desloca_dir_0 0 0 R desloca_dir_0\n")
    f_out.write("desloca_dir_0 1 0 R desloca_dir_1\n")
    f_out.write("desloca_dir_0 _ 0 L volta_cursor\n\n")
    f_out.write("desloca_dir_1 0 1 R desloca_dir_0\n")
    f_out.write("desloca_dir_1 1 1 R desloca_dir_1\n")
    f_out.write("desloca_dir_1 _ 1 L volta_cursor\n\n")
    f_out.write("volta_cursor 0 0 L volta_cursor\n")
    f_out.write("volta_cursor 1 1 L volta_cursor\n")
    f_out.write("volta_cursor # # R 0_inf\n\n")

    estadosVisitados = []
    estadosAVisitar = []
    
    for line in linhas:
        original_line = line.strip()
        if not original_line:
            f_out.write("\n")
            continue
        
        code = original_line
        if ";" in original_line:
            code = original_line.split(";", 1)[0].strip()

        if not code:
            continue
        
        partes = code.split()
        if not partes: continue

        estado_inicial = partes[0]
        estado_final = partes[4]

        if estado_inicial not in estadosVisitados:
            estadosVisitados.append(estado_inicial)
            f_out.write(f"{estado_inicial}_inf # # R {estado_inicial}_inf\n")
            
        if "halt" not in estado_final and estado_final not in estadosAVisitar:
            estadosAVisitar.append(estado_final)

        partes[0] = f"{estado_inicial}_inf"
        if "halt" not in estado_final:
            partes[4] = f"{estado_final}_inf"
        
        f_out.write(" ".join(partes))
        f_out.write("\n")
    
    for estado in estadosAVisitar:
        if estado not in estadosVisitados:
            f_out.write(f"\n{estado}_inf # # R {estado}_inf\n")

def converter_para_sipser(f_out, linhas):
    f_out.write("0 0 # R prepara_0\n")
    f_out.write("0 1 # R prepara_1\n")
    f_out.write("0 _ # R marca_final\n\n")
    f_out.write("prepara_0 0 0 R prepara_0\n")
    f_out.write("prepara_0 1 0 R prepara_1\n")
    f_out.write("prepara_0 _ 0 R marca_final\n\n")
    f_out.write("prepara_1 0 1 R prepara_0\n")
    f_out.write("prepara_1 1 1 R prepara_1\n")
    f_out.write("prepara_1 _ 1 R marca_final\n\n")
    f_out.write("marca_final _ & L volta_inicio\n\n")
    f_out.write("volta_inicio 0 0 L volta_inicio\n")
    f_out.write("volta_inicio 1 1 L volta_inicio\n")
    f_out.write("volta_inicio # # R 0_sip\n\n")

    estadosVisitados = []
    estadosAVisitar = []
    
    for line in linhas:
        original_line = line.strip()
        if not original_line:
            f_out.write("\n")
            continue

        code = original_line
        if ";" in original_line:
            code = original_line.split(";", 1)[0].strip()

        if not code:
            continue
        
        partes = code.split()
        if not partes: continue

        estado_inicial = partes[0]
        estado_final = partes[4]

        if estado_inicial not in estadosVisitados:
            estadosVisitados.append(estado_inicial)
            f_out.write(f"{estado_inicial}_sip # # R corr_esq_{estado_inicial}\n")
            f_out.write(f"{estado_inicial}_sip & _ R corr_dir_{estado_inicial}\n")
        
        if "halt" not in estado_final and estado_final not in estadosAVisitar:
            estadosAVisitar.append(estado_final)
            
        partes[0] = f"{estado_inicial}_sip"
        if "halt" not in estado_final:
            partes[4] = f"{estado_final}_sip"
        
        f_out.write(" ".join(partes))
        f_out.write("\n")
    
    todos_estados = list(set(estadosVisitados + estadosAVisitar))
    for estado in todos_estados:
        _escrever_subrotinas_correcao(f_out, estado)

def main():
    arquivos_entrada = sys.argv[1:]

    if not arquivos_entrada:
        arquivos_entrada = [f for f in os.listdir('.') if f.endswith('.in')]
        if not arquivos_entrada:
            print("Nenhum arquivo .in encontrado no diretório.")
            return
        print(f"Nenhum arquivo especificado, processando todos os {len(arquivos_entrada)} arquivos .in encontrados.")

    for arquivo_entrada in arquivos_entrada:
        if not arquivo_entrada.endswith('.in'):
            print(f"Aviso: Arquivo '{arquivo_entrada}' ignorado pois não tem a extensão .in")
            continue
        
        arquivo_saida = os.path.splitext(arquivo_entrada)[0] + '.out'
        print("-" * 30)

        try:
            with open(arquivo_entrada, "r") as f_in:
                linhas = f_in.readlines()
                if not linhas:
                    print(f"Arquivo '{arquivo_entrada}' está vazio.")
                    continue
                
                primeira_linha = linhas[0].upper()
                linhas_conteudo = linhas[1:]

                with open(arquivo_saida, "w+") as f_out:
                    if "S" in primeira_linha:
                        print(f"Convertendo '{arquivo_entrada}' (Sipser) para '{arquivo_saida}' (Dupla-Infinita)...")
                        converter_para_infinita(f_out, linhas_conteudo)
                        print("Conversão concluída.")
                    elif "I" in primeira_linha:
                        print(f"Convertendo '{arquivo_entrada}' (Dupla-Infinita) para '{arquivo_saida}' (Sipser)...")
                        converter_para_sipser(f_out, linhas_conteudo)
                        print("Conversão concluída.")
                    else:
                        print(f"A primeira linha de '{arquivo_entrada}' deve conter 'S' ou 'I'.")
        
        except FileNotFoundError:
            print(f"Arquivo '{arquivo_entrada}' não encontrado.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado ao processar '{arquivo_entrada}': {e}")

if __name__ == "__main__":
    main()
