import tkinter as tk
from tkinter import messagebox
from Banco_IMC import Banco_IMC

STANDARD_FONT = ("Arial",10)
HEADER_FONT = ("Arial",11)
STANDARD_BOX_SIZE = 20

class IMC(tk.Frame):

    def __init__(self,master=None):
        #Inheritance of Tk and its constructor
        super().__init__(master)
        self.Id = 0
        self.bd = Banco_IMC()
        self.master= master
        self.grid(row=0,column=0)
        #Blocking the user interferance on window size
        self.master.resizable(width=False, height=False)
        self.create_widgets()   

    def create_widgets(self):
        #Declaration
        #Labels
        self.winfo_toplevel().title("Cálculo do IMC - Índice de Massa Corporal")
        self.lb_empty = tk.Label(self, text=" ", font=HEADER_FONT)
        self.lb_name = tk.Label(self, text="Nome do Paciente", font=STANDARD_FONT)
        self.lb_address = tk.Label(self, text="Endereço Completo", font=STANDARD_FONT)
        self.lb_height = tk.Label(self, text="Altura (cm)", font=STANDARD_FONT)
        self.lb_weight = tk.Label(self, text="Peso (kg)", font=STANDARD_FONT)
        self.lb_IMC_result = tk.Label(self, text="-", font=STANDARD_FONT, width=STANDARD_BOX_SIZE, borderwidth=1, relief="solid")
        #Entry Points
        self.et_name = tk.Entry(self, width=STANDARD_BOX_SIZE)
        self.et_address = tk.Entry(self, width=STANDARD_BOX_SIZE)
        self.et_height = tk.Entry(self, width=STANDARD_BOX_SIZE)
        self.et_weight = tk.Entry(self, width=STANDARD_BOX_SIZE)
        #Buttons
        self.bt_calculate = tk.Button(self, text="Calcular", command=self.return_IMC, width=STANDARD_BOX_SIZE)
        self.bt_restart = tk.Button(self, text="Reiniciar", command=self.restart, width=STANDARD_BOX_SIZE)
        self.bt_exit = tk.Button(self, text ="Sair", command=self.exit, width=STANDARD_BOX_SIZE)
        self.bt_record = tk.Button(self, text ="Gravar novo", command=self.record, width=STANDARD_BOX_SIZE)
        self.bt_next = tk.Button(self, text =">", command=self.next, width=10)
        self.bt_previous = tk.Button(self, text ="<", command=self.previous, width=10)
        
        #Placing
        #Labels
        self.lb_empty.grid(row=0, column=0, sticky="WESN", columnspan=2)
        self.lb_name.grid(row=2, column=0)
        self.lb_address.grid(row=3, column=0)
        self.lb_height.grid(row=4,column=0)
        self.lb_weight.grid(row=5, column=0)
        self.lb_IMC_result.grid(row=4,column=2,rowspan=2,columnspan=4,sticky="WESN",padx=10)
        #Entry Points
        self.et_name.grid(row=2,column=1, columnspan=5, sticky="WE",padx=10,pady=10)
        self.et_address.grid(row=3,column=1, columnspan=5, sticky="WE",padx=10,pady=10)
        self.et_height.grid(row=4,column=1,sticky="WN",padx=10,pady=10)
        self.et_weight.grid(row=5, column=1,sticky="WN",padx=10,pady=10)
        #Buttons
        self.bt_calculate.grid(row=7, column=1, sticky="E")
        self.bt_restart.grid(row=7, column=2, sticky="E")
        self.bt_exit.grid(row=7,column=4,columnspan=2, sticky="E",padx=10,pady=10)
        self.bt_record.grid(row=8, column=2, sticky="E",padx=20,pady=10)
        self.bt_next.grid(row=8,column=5, sticky="W",padx=10,pady=10)
        self.bt_previous.grid(row=8,column=4, sticky="E")
        
    def return_IMC(self):
        #This functions returns the IMC with its description.
        calculated_IMC = self.calculate()
        answer = str(calculated_IMC) + ", "
        if calculated_IMC == -1:
            tk.messagebox.showwarning("Erro","Valor(es) inserido(s) inválido(s), tente novamente")
            self.lb_IMC_result["text"]= "-"
            return
        elif calculated_IMC < 18.50:
            answer = answer + "abaixo do peso"
        elif calculated_IMC < 25.00:
            answer = answer + "peso normal"
        elif calculated_IMC < 30.00:
            answer = answer + "sobrepeso"
        elif calculated_IMC < 35.00:
            answer = answer + "obesidade grau 1"
        elif calculated_IMC < 40.00:
            answer = answer + "obesidade grau 2"
        else:
            answer = answer + "obesidade grau 3"

        self.lb_IMC_result["text"]= answer
        
    def calculate(self):
        #This function returns the IMC value, using height in centimeters and
        #weight in kilograms, rounding to 2 decimal cases.
        #If a non integer value is informed, it returns -1.
        if (str(self.et_weight.get()).isnumeric() and
           str(self.et_height.get()).isnumeric()):
               calculated_IMC = (int(self.et_weight.get())/(int(self.et_height.get())/100)**2)   
               return round(calculated_IMC,2)
        else:
            return -1
    
    def restart(self):
        self.et_name.delete(0,'end')
        self.et_address.delete(0,'end')
        self.et_height.delete(0,'end')
        self.et_weight.delete(0,'end')
        self.lb_IMC_result["text"]= "-"

    def exit(self):
        root.destroy();

    def record(self):
        try:
            self.bd.insert(self.et_name.get(),
                          self.et_address.get(),
                          int(self.et_weight.get()),
                          int(self.et_height.get()))
            tk.messagebox.showinfo("IMC", "Gravação feita com sucesso, use as setas para navegar pelos pacientes que já gravou")
        except:
            tk.messagebox.showerror("IMC", "Ocorreu um erro ao gravar, verifique os valores inseridos.")
            
    def next(self):
        data = self.bd.return_by_id(self.Id+1)
        if not data is None:
            self.et_name.delete(0,'end')
            self.et_address.delete(0,'end')
            self.et_weight.delete(0,'end')
            self.et_height.delete(0,'end')
            
            self.et_name.insert(0,data[1])
            self.et_address.insert(0,data[2])
            self.et_weight.insert(0,data[3])
            self.et_height.insert(0,data[4])
            self.return_IMC()
            self.Id += 1
            
            
    def previous(self):
        data = self.bd.return_by_id(self.Id-1)
        if not data is None:
            self.et_name.delete(0,'end')
            self.et_address.delete(0,'end')
            self.et_weight.delete(0,'end')
            self.et_height.delete(0,'end')
            
            self.et_name.insert(0,data[1])
            self.et_address.insert(0,data[2])
            self.et_weight.insert(0,data[3])
            self.et_height.insert(0,data[4])
            self.return_IMC()
            self.Id -= 1
       
        
root = tk.Tk()
app = IMC(root)
app.mainloop()

