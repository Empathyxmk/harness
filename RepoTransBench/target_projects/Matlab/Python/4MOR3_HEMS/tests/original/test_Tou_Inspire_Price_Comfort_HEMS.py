import numpy as np
from src.hems.Tou_Inspire_Price_Comfort_HEMS import Tou_Inspire_Price_Comfort_HEMS

def test_Tou_Inspire_Price_Comfort_HEMS_basic():
    N_T = 24
    Gen_PV = np.random.rand(N_T) * 5  # kW
    Load_HVAC = np.random.rand(N_T) * 3
    Load_EV = np.zeros(N_T)
    Load_EV[9:14] = 2  # indices 9-13, as Python is 0-based
    Load_HW = np.random.rand(N_T) * 1
    Load_Rigid = np.random.rand(N_T) * 2
    Buy_Price = np.random.rand(N_T) * 0.2 + 0.1
    Sell_Price = np.random.rand(N_T) * 0.1 + 0.05
    T_out = 10 + np.random.rand(N_T) * 20
    Tem_Indoor_Up = 26
    Tem_Indoor_Low = 20
    Initial_SOC_Bat = 0.5
    Initial_SOC_EV = 0.3
    Initial_SOC_HW = 0.6
    T_Min_HW = 50
    T_Max_HW = 60
    T_setpoint_HW = 55
    R_in = 0.01
    C_in = 1000
    R_out = 0.02
    C_out = 500
    T_setpoint_HVAC = 22
    
    # Call function
    (
        Total_Cost, SOC_Bat, Load_Curve, SOC_EV, SOC_HW, 
        P_PV, P_Grid, Price_ToU, Comfort_index
    ) = Tou_Inspire_Price_Comfort_HEMS(
        Gen_PV, Load_HVAC, Load_EV, Load_HW, Load_Rigid,
        Buy_Price, Sell_Price, T_out, Tem_Indoor_Up, Tem_Indoor_Low,
        Initial_SOC_Bat, Initial_SOC_EV, Initial_SOC_HW, T_Min_HW,
        T_Max_HW, T_setpoint_HW, R_in, C_in, R_out, C_out, T_setpoint_HVAC
    )
    assert isinstance(Total_Cost, float) or np.isscalar(Total_Cost)
    assert len(SOC_Bat) == N_T
    assert np.all((SOC_Bat >= 0) & (SOC_Bat <= 1))
    assert len(Load_Curve) == N_T
    assert len(P_Grid) == N_T
    assert len(Comfort_index) == N_T

def test_Tou_Inspire_Price_Comfort_HEMS_zero_pv():
    N_T = 24
    Gen_PV = np.zeros(N_T)
    Load_HVAC = np.random.rand(N_T) * 3
    Load_EV = np.zeros(N_T)
    Load_EV[9:14] = 2  # as above
    Load_HW = np.random.rand(N_T) * 1
    Load_Rigid = np.random.rand(N_T) * 2
    Buy_Price = np.random.rand(N_T) * 0.2 + 0.1
    Sell_Price = np.random.rand(N_T) * 0.1 + 0.05
    T_out = 10 + np.random.rand(N_T) * 20
    Tem_Indoor_Up = 26
    Tem_Indoor_Low = 20
    Initial_SOC_Bat = 0.5
    Initial_SOC_EV = 0.3
    Initial_SOC_HW = 0.6
    T_Min_HW = 50
    T_Max_HW = 60
    T_setpoint_HW = 55
    R_in = 0.01
    C_in = 1000
    R_out = 0.02
    C_out = 500
    T_setpoint_HVAC = 22

    (Total_Cost, *_rest) = Tou_Inspire_Price_Comfort_HEMS(
        Gen_PV, Load_HVAC, Load_EV, Load_HW, Load_Rigid,
        Buy_Price, Sell_Price, T_out, Tem_Indoor_Up, Tem_Indoor_Low,
        Initial_SOC_Bat, Initial_SOC_EV, Initial_SOC_HW, T_Min_HW,
        T_Max_HW, T_setpoint_HW, R_in, C_in, R_out, C_out, T_setpoint_HVAC
    )
    assert isinstance(Total_Cost, float) or np.isscalar(Total_Cost)