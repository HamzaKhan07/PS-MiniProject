from sklearn import linear_model
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()

cgpa = tk.StringVar()
root.configure(bg='white')
canvas = tk.Canvas(width=600, height=350, bg='white', borderwidth=0, highlightthickness=0)
canvas.grid(columnspan=3, rowspan=3)

x_test=np.array([[]])
y_test=np.array([[]])
y_predict=np.array([[]])

# functions
def check_valid(val):
    try:
        float(val)
        return True
    except ValueError:
        return False

def predict_score():
    global x_test, y_test, y_predict

    score=cgpa.get()

    if not check_valid(score):
        tk.messagebox.showwarning("Invalid value", "Please enter numeric values.")
        prediction_text.set(' ')
        x_test = np.array([[]])
        y_test = np.array([[]])
        y_predict = np.array([[]])
    elif float(score) > 10 or float(score) < 1:
        tk.messagebox.showwarning("Invalid value", "CGPA must be > 1 and < 10.")
        prediction_text.set(' ')
        x_test = np.array([[]])
        y_test = np.array([[]])
        y_predict = np.array([[]])
    else:
        # read data
        data=pd.read_excel('Survey.xlsx')

        # extract specific cols
        cgpa_fy_data=data['CGPA-1year']
        sgpa_sy_sem1_data=data['SGPA-SY-Sem1']

        # convert series into dataframe
        cgpa_fy_x=cgpa_fy_data.to_numpy()
        cgpa_fy_x=cgpa_fy_x.reshape(-1, 1)

        sgpa_sy1_y=sgpa_sy_sem1_data.to_numpy()
        sgpa_sy1_y=sgpa_sy1_y.reshape(-1, 1)

        # separate test data and training data
        cgpa_fy_x_train=cgpa_fy_x[-30:]
        cgpa_fy_x_test=cgpa_fy_x[0: 30]

        sgpa_sy1_y_train=sgpa_sy1_y[-30:]
        sgpa_sy1_y_test=sgpa_sy1_y[0:30]

        model=linear_model.LinearRegression()
        model.fit(cgpa_fy_x_train, sgpa_sy1_y_train)

        sgpa_sy1_y_predict=model.predict(cgpa_fy_x_test)

        # custom prediction here
        custom_prediction=model.predict(np.array([[score]], dtype='float'))
        # print('Custom Prediction: ',custom_prediction)
        prediction_score=(custom_prediction[0][0])
        prediction_score=round(prediction_score, 2)
        prediction_text.set(prediction_score)

        # derive metrics
        # print('Mean squared error: ', mean_squared_error(sgpa_sy1_y_test, sgpa_sy1_y_predict))
        # print('Weight: ', model.coef_)
        # print('Intercept: ', model.intercept_)

        # plot
        x_test=cgpa_fy_x_test
        y_test=sgpa_sy1_y_test
        y_predict=sgpa_sy1_y_predict

def plot_graph():
    global x_test, y_test, y_predict

    if x_test.size > 0 and y_test.size > 0 and y_predict.size > 0:
        plt.scatter(x_test, y_test)
        plt.plot(x_test, y_predict)
        plt.plot()
        plt.show()
    else:
        print('empty values')
        tk.messagebox.showinfo("Use \"Predict\" First", "Please Use Predict function first to Plot Graph.")


# logo
logo = Image.open('images/logo.png')
logo = ImageTk.PhotoImage(logo)
logoLabel = tk.Label(image=logo, borderwidth=0, highlightthickness=0)
logoLabel.image = logo
logoLabel.grid(row=0, column=1, pady=0)

# Label
label1 = tk.Label(root, text='Enter CGPA of FY', font='Poppins 13', bg='white')
label1.grid(columnspan=3, row=1, column=0, pady=0)

# other canvas
canvas = tk.Canvas(width=600, height=220, bg='white', borderwidth=0, highlightthickness=0)
canvas.grid(columnspan=3, rowspan=3)

# input
entry = tk.Entry(root, textvariable=cgpa, font=('Poppins', 16, 'normal'), bg='#F0F0F0', borderwidth=0, highlightthickness=0)
entry.grid(columnspan=3, row=2, column=0, ipadx=50, ipady=10, pady=10)

# buttons
predict_btn = tk.Button(root, text='Predict',command=predict_score, font='Poppins 12 bold', bg='#20bebe', fg='white',
                        height=1, width=15)
predict_btn.grid(row=3, column=1)

plot_btn = tk.Button(root, text='Plot', command=plot_graph, font='Poppins 12 bold', bg='#E4E4E4', fg='#484848',
                     height=1, width=15)
plot_btn.grid(row=4, column=1)

# last canvas
canvas = tk.Canvas(width=600, height=200, bg='white', borderwidth=0, highlightthickness=0)
canvas.grid(columnspan=3, rowspan=3)

label2 = tk.Label(root, text='Predicted SY SGPA Score', font='Poppins 13', bg='white')
label2.grid(columnspan=3, row=5, column=0)

# prediction score
prediction_text=tk.StringVar()
prediction_text.set(' ')
label2 = tk.Label(root, textvariable=prediction_text, font='Poppins 50 bold', bg='white')
label2.grid(columnspan=3, row=6, column=0)


root.mainloop()
