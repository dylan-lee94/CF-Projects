
# %% Imports
import math as m
from prettytable import PrettyTable

# %%
# Functions to read user input under certain conditions
# More constrain can be easily added, but left it simple for now

def inputFloat(message):
  while True:
    try:
       userInput = float(input(message))       
    except ValueError:
       print("This is not a Number! Please try again")
       continue
    else:
        if userInput >= 0:
            return userInput
            break
        else:
            print("Number must be larger or equal to Zero! Please try again")
            continue

# Defining a input function, to collectively read all variables
def input_func():
    stock=inputFloat("Enter the stock price: ")
    strike=inputFloat("Enter the strike: ")
    r=inputFloat("Enter the risk-free rate is (in decimal): ")
    div=inputFloat("Enter Dividend yield (in decimal): ")
    sigma=inputFloat("Enter the the volatility (in decimal): ")
    tau=inputFloat("Enter time to expiry [0,1]: ")
    return stock,div,strike,r,tau,sigma

# %%

# This Output functions calls the functions calculating Put and Call values and prints the results to the screen

def output(d1,d2,stock,div,strike,r,tau,sigma):
    t = PrettyTable(['Option','Call', 'Put'])
    t.align["Vanilla Option"] = "l"

    t.add_row(['The option value is:', call_option(d1,d2,stock,div,strike,r,tau,sigma),put_option(d1,d2,stock,div,strike,r,tau,sigma)])
    t.add_row(['The delta is ', delta_call(d1,div,tau),delta_put(d1,div,tau)])
    t.add_row(['The theta is ', theta_call(d1,d2,stock,div,strike,r,tau,sigma),theta_put(d1,d2,stock,div,strike,r,tau,sigma)])
    t.add_row(['The vega is ', vega_call(d1,stock,div,tau),vega_put(d1,stock,div,tau)])
    t.add_row(['The rho is ', rho_call(d2,strike,r,tau),rho_put(d2,strike,r,tau)])
    print(t)

# This Output functions calls the functions calculating Put and Call values and prints the results to the screen

def output_binary(d1,d2,stock,div,strike,r,tau,sigma):
    t = PrettyTable(['Binary Option','Call', 'Put'])
    t.align["Binary Option"] = "l"
    t.add_row(['The option value is:', binary_call_option(d2,r,tau),binary_put_option(d2,r,tau)])
    t.add_row(['The delta is ', delta_binary_call(d2,stock,r,tau,sigma),delta_binary_put(d2,stock,r,tau)])
    t.add_row(['The theta is ', theta_binary_call(d1,d2,div,r,tau,sigma),theta_binary_put(d1,d2,div,r,tau,sigma)])
    t.add_row(['The vega is ', vega_binary_call(d2,r,tau,sigma),vega_binary_put(d2,r,tau,sigma)])
    t.add_row(['The rho is ', rho_binary_call(d2,r,tau,sigma),rho_binary_put(d2,r,tau,sigma)])
    print(t)

# %%
# Normal CDF
def CDF(X):
    (a1,a2,a3,a4,a5) = (0.319381530, -0.356563782, 1.781477937, -1.821255978, 1.330274429)
    x=abs(X)
    k=1/(1+0.2316419*x)
    n=(1/m.sqrt(2*m.pi))*m.exp(-0.5*x**2)
    N=1.0-n*(a1*k+a2*k**2+a3*pow(k,3)+a4*pow(k,4)+a5*pow(k,5))
    if X<0:
        N=1.0-N
    return N


# Normal PDF
def PDF(X):
    N = 1/(m.sqrt(2*m.pi))*m.exp(-pow(X,2)/2)
    return N

# Defining d1
def d1_func(stock,div,strike,r,tau,sigma):
    Moneyness=m.log(stock/strike,m.e)
    shift=r-div+0.5*sigma**2
    d1=(Moneyness+shift*tau)/(sigma*m.sqrt(tau))
    return d1

# Defining d2
def d2_func(d1,sigma,tau):
    d2=d1-sigma*m.sqrt(tau)
    return d2


# Black-Scholes pricing formula for Call and Put
def call_option(d1,d2,stock,div,strike,r,tau,sigma):
    call=stock*m.exp(-div*tau)*CDF(d1)-m.exp(-r*tau)*strike*CDF(d2)
    return round(call,5)

def put_option(d1,d2,stock,div,strike,r,tau,sigma):
    put=-stock*m.exp(-div*tau)*CDF(-d1)+m.exp(-r*(tau))*strike*CDF(-d2)
    return round(put,5)


# Black-Scholes pricing formula for Binary Call and Binary Put
def binary_call_option(d2,r,tau):
    binary_call = m.exp(-r*tau)*CDF(d2)
    return round(binary_call,5)

def binary_put_option(d2,r,tau):
    binary_put = m.exp(-r*tau)*CDF(-d2)
    return round(binary_put,5)

# %%
# All the Greeks defined for Call and Put
def delta_call(d1,div,tau):
    call_delta = m.exp(-div*tau)*CDF(d1)
    return round(call_delta,5)
    
def delta_put(d1,div,tau):
    put_delta = m.exp(-div*tau)*(CDF(d1)-1)
    return round(put_delta,5)
    
def theta_call(d1,d2,stock,div,strike,r,tau,sigma):
    call_theta = -(sigma*stock*m.exp(-div*tau))/(2*m.sqrt(tau)) *PDF(d1)        + div*stock*CDF(d1)*m.exp(-div*tau)        - r*strike*m.exp(-r*tau)*CDF(d2)
    return round(call_theta,5)
    
def theta_put(d1,d2,stock,div,strike,r,tau,sigma):
    put_theta  = -(sigma*stock*m.exp(-div*tau))/(2*m.sqrt(tau)) *PDF(-d1)        - div*stock*CDF(-d1)*m.exp(-div*tau)        + r*strike*m.exp(-r*tau)*CDF(-d2)
    return round(put_theta,5)

def vega_call(d1,stock,div,tau):
    call_vega = stock*m.sqrt(tau)*m.exp(-div*tau)*PDF(d1)
    return round(call_vega,5)

def vega_put(d1,stock,div,tau):
    put_vega = stock*m.sqrt(tau)*m.exp(-div*tau)*PDF(d1)
    return round(put_vega,5)

    
def rho_call(d2,strike,r,tau):
    call_rho = strike*tau*m.exp(-r*tau)*CDF(d2)
    return round(call_rho,5)

def rho_put(d2,strike,r,tau):
    put_rho = -strike*tau*m.exp(-r*tau)*CDF(-d2)
    return round(put_rho,5)

# All the Greeks defined for Binary Call and Binary Put
def delta_binary_call(d2,stock,r,tau,sigma):
    bin_call_delta = m.exp(-r*tau)/(sigma*stock*m.sqrt(tau))*PDF(d2)
    return round(bin_call_delta,5)

def delta_binary_put(d2,stock,r,tau):
    bin_put_delta = -m.exp(-r*tau)/(sigma*stock*m.sqrt(tau))*PDF(d2)
    return round(bin_put_delta,5)

def theta_binary_call(d1,d2,div,r,tau,sigma):
    bin_call_theta = r*m.exp(-r*tau)*CDF(d2)        +m.exp(-r*tau)*PDF(d2)*(d1/(2*tau) - (r-div)/(sigma*m.sqrt(tau)))
    return round(bin_call_theta,5)

def theta_binary_put(d1,d2,div,r,tau,sigma):
    bin_put_theta = r*m.exp(-r*tau)*(1-CDF(d2))        -m.exp(-r*tau)*PDF(d2)*(d1/(2*tau) - (r-div)/(sigma*m.sqrt(tau)))
    return round(bin_put_theta,5)

def vega_binary_call(d2,r,tau,sigma):
    bin_call_vega = -m.exp(-r*tau)*PDF(d2)*(m.sqrt(tau)+d2/sigma)
    return round(bin_call_vega,5)

def vega_binary_put(d2,r,tau,sigma):
    bin_put_vega = m.exp(-r*tau)*PDF(d2)*(m.sqrt(tau)+d2/sigma)
    return round(bin_put_vega,5)

def rho_binary_call(d2,r,tau,sigma):
    bin_call_rho = -tau*m.exp(-r*tau)*CDF(d2)+m.sqrt(tau)/sigma*m.exp(-r*tau)*PDF(d2)
    return round(bin_call_rho,5)

def rho_binary_put(d2,r,tau,sigma):
    bin_put_rho = -tau*m.exp(-r*tau)*(1-CDF(d2))-m.sqrt(tau)/sigma*m.exp(-r*tau)*PDF(d2)
    return round(bin_put_rho,5)

# %%
# Main Body

if __name__ == '__main__':
    #Get the Input from the user
    stock,div,strike,r,tau,sigma =input_func() 

    #Compute d1 and d2
    d1=d1_func(stock,div,strike,r,tau,sigma)
    d2=d2_func(d1,sigma,tau)
        
    #Generate screen output by using the formulas
    output(d1,d2,stock,div,strike,r,tau,sigma)
    output_binary(d1,d2,stock,div,strike,r,tau,sigma)


