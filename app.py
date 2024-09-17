import tkinter as tk
from tkinter import ttk, messagebox
import locale
import re

# Configura o locale para formato de moeda brasileira
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Função para formatar números como moeda em reais
def formatar_moeda(valor):
    try:
        # Remove caracteres não numéricos e formata como moeda
        valor = re.sub(r'[^\d]', '', valor)
        valor_float = float(valor) / 100
        return locale.currency(valor_float, grouping=True)
    except ValueError:
        return ""

# Função para atualizar o campo com formatação em tempo real
def atualizar_formato(event):
    valor = event.widget.get()
    valor_formatado = formatar_moeda(valor)
    event.widget.delete(0, tk.END)
    event.widget.insert(0, valor_formatado)

# Função para calcular a carga tributária do Simples Nacional
def simples_nacional(faturamento):
    faixas = [
        (180000, 0.06),   # Faturamento até 180 mil
        (360000, 0.112),  # Faturamento até 360 mil
        (720000, 0.135),  # Faturamento até 720 mil
        (1800000, 0.16),  # Faturamento até 1.8 milhão
        (3600000, 0.21),  # Faturamento até 3.6 milhões
        (4800000, 0.23)   # Faturamento até 4.8 milhões
    ]
    
    for limite, aliquota in faixas:
        if faturamento <= limite:
            return faturamento * aliquota
    return None

# Função para calcular a carga tributária do Lucro Presumido
def lucro_presumido(faturamento, setor):
    if setor == "comércio":
        presuncao = 0.08
    elif setor == "serviços":
        presuncao = 0.32
    else:
        presuncao = 0.16
    
    base_calculo = faturamento * presuncao
    irpj = base_calculo * 0.15
    csll = base_calculo * 0.09
    
    total_impostos = irpj + csll
    return total_impostos

# Função para calcular a carga tributária do Lucro Real
def lucro_real(lucro_liquido):
    irpj = lucro_liquido * 0.15
    adicional_irpj = (lucro_liquido - 240000) * 0.10 if lucro_liquido > 240000 else 0
    csll = lucro_liquido * 0.09
    
    total_impostos = irpj + adicional_irpj + csll
    return total_impostos

# Função para calcular e exibir os resultados
def calcular_imposto():
    try:
        faturamento = float(re.sub(r'[^\d]', '', entry_faturamento.get())) / 100
        setor = setor_var.get()
        regime_tributario = regime_var.get()
        lucro_liquido = None
        
        if regime_tributario == "Lucro Real":
            lucro_liquido = float(re.sub(r'[^\d]', '', entry_lucro_liquido.get())) / 100
        
        if regime_tributario == "Simples Nacional":
            imposto = simples_nacional(faturamento)
            if imposto is not None:
                resultado.set(f"Imposto estimado pelo Simples Nacional: {locale.currency(imposto, grouping=True)}")
            else:
                resultado.set("O faturamento excede o limite do Simples Nacional.")
        elif regime_tributario == "Lucro Presumido":
            imposto = lucro_presumido(faturamento, setor)
            resultado.set(f"Imposto estimado pelo Lucro Presumido: {locale.currency(imposto, grouping=True)}")
        elif regime_tributario == "Lucro Real":
            if lucro_liquido is not None:
                imposto = lucro_real(lucro_liquido)
                resultado.set(f"Imposto estimado pelo Lucro Real: {locale.currency(imposto, grouping=True)}")
            else:
                resultado.set("Por favor, forneça o lucro líquido para o Lucro Real.")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

# Configuração da interface gráfica com Tkinter
root = tk.Tk()
root.title("Planejamento Tributário")
root.geometry("400x400")

# Labels e entradas
ttk.Label(root, text="Faturamento Anual (R$)").pack(pady=5)
entry_faturamento = ttk.Entry(root)
entry_faturamento.pack(pady=5)
entry_faturamento.bind("<KeyRelease>", atualizar_formato)

ttk.Label(root, text="Setor de Atuação").pack(pady=5)
setor_var = tk.StringVar()
ttk.Combobox(root, textvariable=setor_var, values=["comércio", "serviços", "outros"]).pack(pady=5)

ttk.Label(root, text="Regime Tributário").pack(pady=5)
regime_var = tk.StringVar()
ttk.Combobox(root, textvariable=regime_var, values=["Simples Nacional", "Lucro Presumido", "Lucro Real"]).pack(pady=5)

ttk.Label(root, text="Lucro Líquido (apenas para Lucro Real)").pack(pady=5)
entry_lucro_liquido = ttk.Entry(root)
entry_lucro_liquido.pack(pady=5)
entry_lucro_liquido.bind("<KeyRelease>", atualizar_formato)

# Botão para calcular
ttk.Button(root, text="Calcular Imposto", command=calcular_imposto).pack(pady=20)

# Resultado
resultado = tk.StringVar()
resultado_label = ttk.Label(root, textvariable=resultado)
resultado_label.pack(pady=10)

# Iniciar a interface
root.mainloop()
