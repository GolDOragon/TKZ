from tkinter import *
from tkinter.ttk import *


class Interp:
    # x_array = ((for Cu), (for Al), (for steel))
    x_array = (
        (0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5),
        (0.0, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8),
        (0.0, 0.03125, 0.0625, 0.125, 0.1875, 0.25, 0.3125, 0.375, 0.4375, 0.5, 0.5625)
    )
    # y_array = ((a1, y_line1), (a2, y_line2), ...)
    y_array = (
        (0.1, (0.98, 0.98, 0.98, 0.98, 0.965, 0.95, 0.935, 0.91, 0.89, 0.87, 0.845, 0.6)),
        (0.2, (0.97, 0.97, 0.97, 0.97, 0.94, 0.915, 0.89, 0.87, 0.85, 0.83, 0.81, 0.6)),
        (0.3, (0.94, 0.94, 0.94, 0.94, 0.912, 0.885, 0.86, 0.84, 0.82, 0.801, 0.785, 0.6)),
        (0.4, (0.933, 0.933, 0.933, 0.933, 0.9, 0.87, 0.84, 0.815, 0.795, 0.775, 0.76, 0.6)),
        (0.5, (0.915, 0.915, 0.915, 0.915, 0.88, 0.845, 0.815, 0.79, 0.77, 0.751, 0.74, 0.6)),
        (0.8, (0.942, 0.942, 0.942, 0.905, 0.86, 0.825, 0.795, 0.765, 0.74, 0.725, 0.71, 0.6)),
        (0.9, (0.94, 0.94, 0.94, 0.89, 0.84, 0.8, 0.77, 0.74, 0.71, 0.69, 0.68, 0.6)),
        (1, (1.0, 0.96, 0.91, 0.86, 0.815, 0.78, 0.74, 0.715, 0.69, 0.67, 0.65, 0.6))
    )
    a_array = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.8, 0.9, 1)

    def find_a(a_line):
        ln = len(Interp.a_array)
        down_line = 0
        for i in range(ln):
            if Interp.a_array[i] <= a_line:
                down_line = i
            elif Interp.a_array[i] > a_line:
                break
        up_line = (down_line + 1) if down_line != ln - 1 else down_line
        # amount start since zero
        return up_line - 1, down_line - 1

    def find_funcs(alpha, material, abscissa):
        # choice material
        materials = {"cu": 0, "al": 1, "steel": 2}
        mat_num = materials.get(material.lower(), 1)

        upline, downline = Interp.find_a(alpha)
        up_a = Interp.y_array[upline][0]
        down_a = Interp.y_array[downline][0]

        # find nv for up and down lines
        for val_index in range(len(Interp.x_array[mat_num])):
            if Interp.x_array[mat_num][val_index] >= abscissa and val_index != 0:
                x1 = Interp.x_array[mat_num][val_index - 1]
                x2 = Interp.x_array[mat_num][val_index]

                y1 = Interp.y_array[downline][1][val_index - 1]
                y2 = Interp.y_array[downline][1][val_index]
                ydown = y1 + (y2 - y1) / (x2 - x1) * (abscissa - x1)

                y1 = Interp.y_array[upline][1][val_index - 1]
                y2 = Interp.y_array[upline][1][val_index]
                yup = y1 + (y2 - y1) / (x2 - x1) * (abscissa - x1)
                break
            elif abscissa > Interp.x_array[mat_num][-1]:
                # Go out from limits
                ydown = 0.6
                yup = 0.6
                break

        return yup, up_a, ydown, down_a

    def get_nv(abscissa, alpha, material):
        y1, a1, y2, a2 = Interp.find_funcs(alpha, material, abscissa)
        if a1 != a2:
            y = y1 + (y2 - y1) / (a2 - a1) * (alpha - a1)
        else:
            y = y1
        y = float(y)
        return round(y, 4)


class DataHelp:
    material_resis = {'Al': 2.82 * 10 ** (-8),
                      'Cu': 1.72 * 10 ** (-8),
                      'Steel': 10.3 * 10 ** (-8)}


    def choice_arc(voltage, power, sc_place):
        # arc_resist[choice_place][choice_voltage][choice_power]
        arc_resist = (((15, 10, 7, 5, 4, 3), (14, 8, 6, 4.5, 3.5, 2.5), (12, 7, 5, 4, 3, 2)),
                      ((6, 6, 6, 6, 4, 3), (5, 5, 5, 5, 3.5, 2.5), (4, 4, 4, 4, 3, 2)),
                      ((8, 8, 8, 8, 7, 6), (7, 7, 7, 7, 6, 5), (6, 6, 6, 6, 5, 4)))
        choice_voltage = {400: 0, 525: 1, 690: 2}
        choice_power = {250: 0, 400: 1, 630: 2, 1000: 3, 1600: 4, 2500: 5}
        ans = arc_resist[sc_place][choice_voltage.get(voltage, 0)][choice_power.get(power, 0)]
        return ans


class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.createWidget()

    def createWidget(self):
        # general font
        fontType = 'Arial'
        Label(self,
              font=fontType + ' 20',
              text="Исходные данные",
              ).grid(row=0, column=1, columnspan=4, sticky=W)

        # material
        Label(self,
              font=fontType,
              text="Материал провода",
              ).grid(row=1, column=0, columnspan=2, sticky=W)
        self.material = StringVar()
        self.material.set('Al')
        Radiobutton(self,
                    text='Медь',
                    variable=self.material,
                    value='Cu'
                    ).grid(row=1, column=3, sticky=W)
        Radiobutton(self,
                    text='Алюминий',
                    variable=self.material,
                    value='Al'
                    ).grid(row=1, column=4, columnspan=2, sticky=W)
        Radiobutton(self,
                    text='Сталь',
                    variable=self.material,
                    value='Steel'
                    ).grid(row=1, column=6, sticky=W)

        # length of conducter
        Label(self,
              font=fontType,
              text="Длина провода",
              ).grid(row=2, column=0, columnspan=2, sticky=W)
        Label(self,
              font=fontType,
              text="м",
              ).grid(row=2, column=5, sticky=W)
        self.length = Entry(self)
        self.length.grid(row=2, column=3, columnspan=2, sticky=W)

        # square of conducter
        Label(self,
              font=fontType,
              text="Сечение провода",
              ).grid(row=3, column=0, columnspan=2, sticky=W)
        Label(self,
              font=fontType,
              text='кв. мм'
              ).grid(row=3, column=5, columnspan=2, sticky=W)
        self.square = Entry(self)
        self.square.grid(row=3, column=3, columnspan=2, sticky=W)

        # resistance of circuit
        Label(self,
              font=fontType,
              text='Сопротивление "фаза-нуль":',
              ).grid(row=4, column=0, columnspan=2, sticky=W)
        Label(self,
              font=fontType,
              text='активное ',
              ).grid(row=5, column=0, columnspan=2, sticky=N)
        Label(self,
              font=fontType,
              text='    реактивное ',
              ).grid(row=6, column=0, columnspan=2, sticky=N)
        Label(self,
              font=fontType,
              text='Ом'
              ).grid(row=5, column=5, sticky=W)
        Label(self,
              font=fontType,
              text='Ом'
              ).grid(row=6, column=5, sticky=W)
        self.sis_resist = Entry(self)
        self.sis_resist.grid(row=5, column=3, columnspan=2, sticky=W)
        self.sis_xesist = Entry(self)
        self.sis_xesist = Entry(self)
        self.sis_xesist.grid(row=6, column=3, columnspan=2, sticky=W)

        # transformer substation power
        Label(self,
              font=fontType,
              text="Мощность питающего\nтрансформатора",
              ).grid(row=7, column=0, columnspan=2, sticky=W)
        Label(self,
              font=fontType,
              text='кВА'
              ).grid(row=7, column=5, sticky=W)
        self.POWERS = (0, 250, 400, 630, 1000, 1600, 2500)
        self.power = StringVar(self)
        self.power.set(self.POWERS[0])
        OptionMenu(self,
                   self.power,
                   *self.POWERS,
                   ).grid(row=7, column=3, columnspan=2, rowspan=2, sticky=N)
        # self.power = Entry(self)
        # self.power.grid(row=7, column=3, columnspan=2, sticky=W)

        # place of short circuit
        Label(self,
              font=fontType,
              text="Место короткого замыкания",
              ).grid(row=8, column=0, columnspan=2, rowspan=4, sticky=W)
        self.sc_place = StringVar()
        self.sc_place.set(None)
        Radiobutton(self,
                    text='в разделке кабелей',
                    variable=self.sc_place,
                    value=0
                    ).grid(row=8, column=3, columnspan=4, sticky=W)
        Radiobutton(self,
                    text='в шинопроводе ШМА',
                    variable=self.sc_place,
                    value=1
                    ).grid(row=10, column=3, columnspan=4, sticky=W)
        Radiobutton(self,
                    text='КЗ в конце шинопровода ШМА',
                    variable=self.sc_place,
                    value=2
                    ).grid(row=11, column=3, columnspan=4, sticky=W)

        # Circuit voltage
        Label(self,
              font=fontType,
              text="Номинальное напряжение\nсети",
              ).grid(row=12, column=0, columnspan=2, sticky=W)
        self.voltage = StringVar()
        self.voltage.set(None)
        Radiobutton(self,
                    text='400 В',
                    variable=self.voltage,
                    value='400'
                    ).grid(row=12, column=3, sticky=W)
        Radiobutton(self,
                    text='525 В',
                    variable=self.voltage,
                    value='525'
                    ).grid(row=12, column=4, columnspan=1, sticky=W)
        Radiobutton(self,
                    text='690 В',
                    variable=self.voltage,
                    value='690'
                    ).grid(row=12, column=5, columnspan=2, sticky=W)

        # Conductor temperature
        Label(self,
              font=fontType,
              text='Температура проводника',
              ).grid(row=13, column=0, columnspan=2, sticky=W)
        Label(self,
              font=fontType,
              text='C'
              ).grid(row=13, column=5, columnspan=2, sticky=W)
        self.temperature = Entry(self)
        self.temperature.insert(0, 20)
        self.temperature.grid(row=13, column=3, columnspan=2, sticky=W)

        # SC time
        Label(self,
              font=fontType,
              text='Время КЗ'
              ).grid(row=14, column=0, columnspan=2, sticky=W)
        self.time = Entry(self)
        self.time.insert(0, 0.1)
        self.time.grid(row=14, column=3, columnspan=2, sticky=W)
        Label(self,
              font=fontType,
              text='c'
              ).grid(row=14, column=5, columnspan=2, sticky=W)

        # Get answer
        Label(self).grid(row=14, column=0)
        Label(self,
              font=fontType + ' 20',
              text='А'
              ).grid(row=15, column=5, sticky=W)
        self.bttn = Button(self,
                           text="Вычислить ток",
                           command=self.data_processing)
        self.bttn.grid(row=15, column=0, columnspan=3, rowspan=3, sticky=N)
        self.answer = Text(self, width=8, height=0.5, font=fontType + ' 20')
        self.answer.grid(row=15, column=3, columnspan=6, rowspan=2, sticky=W)

        # default values
        self.bttn2 = Button(self,
                           text="Cброс",
                           command=self.restart)
        self.bttn2.grid(row=18, column=0, columnspan=3, sticky=N)

    def restart(self):
        for var in (self.length, self.square, self.sis_resist,
                    self.sis_xesist, self.temperature, self.time):
            var.delete(0, END)
        self.material.set('Al')
        self.power.set(self.POWERS[0])
        self.sc_place.set(None)
        self.voltage.set(None)
        self.temperature.insert(0, 20)
        self.time.insert(0, 0.1)


    def data_processing(self):
        material = self.material.get()
        length = float(self.length.get())  # m
        square = float(self.square.get())  # mm^2
        sis_resist = float(self.sis_resist.get())  # Om
        power = float(self.power.get())  # kVA
        voltage = float(self.voltage.get())  # V or kV
        sc_place = int(self.sc_place.get())  # для выбора в таблице сопротивлений дуг
        temperature = float(self.temperature.get())  # Cel
        sis_xesist = float(self.sis_xesist.get())  # Om
        time = float(self.time.get())  # sec

        conducter_xesist = 0  # Om
        # conducter resistance Om
        conducter_resist = (DataHelp.material_resis.get(material) * 2 * length) / (square * 10 ** (-6)) * (
                1 + 0.004 * (20 - temperature))

        # arc resistance Om
        arc_resist = DataHelp.choice_arc(voltage, power, sc_place) / 1000

        # curcuit current A
        i_curcuit = voltage / (3 ** 0.5 * (conducter_resist + sis_resist))

        # delta for 0.1 sec    (A*sec)^2 / mm^4
        dlt = (i_curcuit / square) ** 2 * time

        # alpha  p.u.
        alpha = ((sis_resist + conducter_resist) / (sis_xesist ** 2 + (sis_resist + conducter_resist) ** 2) ** 0.5) ** 2

        # nv    p.u
        nv = Interp.get_nv(dlt / 1000, alpha, material)

        # final current for [time] sec
        i_kz = (0.95 * nv * voltage * 3 ** 0.5) / ((3 * (sis_resist + conducter_resist) + arc_resist) ** 2 + 9 * (
                sis_xesist + conducter_xesist) ** 2) ** 0.5
        i_kz = round(i_kz, 4)
        self.answer.delete(0.0, END)
        self.answer.insert(0.0, i_kz)


if __name__ == '__main__':
    root = Tk()
    root.title('ТКЗ')
    root.geometry('445x420')
    app = Application(root)
    root.mainloop()
