#include <iostream>
#include <math.h>
#include <fstream>
#include <string>
using namespace std;

class SimpleKalmanFilter 
{

public:
  SimpleKalmanFilter(float mea_e, float est_e, float q);
  float updateEstimate(float mea);
  void setMeasurementError(float mea_e);
  void setEstimateError(float est_e);
  void setProcessNoise(float q);
  float getKalmanGain();
  
private:
  float _err_measure; // R measurement noise covariance
  float _err_estimate; // Pk estimation error covariance
  float _q; // Q estimation error covariance
  float _current_estimate; // x filtered value
  float _last_estimate; // x
  float _kalman_gain; // k

};
//--------------------------------------------------------------------------------------
SimpleKalmanFilter::SimpleKalmanFilter(float mea_e, float est_e, float q) // ham dinh nghia va cho cac bien bang voi bien cua cac ham tinh toan
{
  _err_measure=mea_e; // e_mea: Measurement Uncertainty - How much do we expect to our measurement vary
  _err_estimate=est_e; // e_est: Estimation Uncertainty - Can be initilized with the same value as e_mea since the kalman filter will adjust its value.
  _q = q; // Process Variance - usually a small number between 0.001 and 1 - how fast your measurement moves. Recommended 0.01. Should be tunned to your needs.
}

float SimpleKalmanFilter::updateEstimate(float mea) // thuat toan kalman tra ve gia tri "filtered value"
{
  _kalman_gain = _err_estimate/(_err_estimate + _err_measure);
  _current_estimate = _last_estimate + _kalman_gain * (mea - _last_estimate); // mea chinh la "z", the measurement (input)
  _err_estimate =  (1.0 - _kalman_gain)*_err_estimate + fabs(_last_estimate-_current_estimate)*_q;
  _last_estimate=_current_estimate;

  return _current_estimate;
}

void SimpleKalmanFilter::setMeasurementError(float mea_e) // set custom gia tri tren code main neu can
{
  _err_measure=mea_e;
}

void SimpleKalmanFilter::setEstimateError(float est_e) // set custom gia tri tren code main neu can
{
  _err_estimate=est_e;
}

void SimpleKalmanFilter::setProcessNoise(float q) // set custom gia tri tren code main neu can
{
  _q=q;
}

float SimpleKalmanFilter::getKalmanGain() { // ham lay gia tri kalman
  return _kalman_gain;
}
//------------------------------------------------------------------------------------------
int main()
{
  SimpleKalmanFilter bo_loc(2, 2, 0.01);
  SimpleKalmanFilter bo_loc2(0.5, 0.5, 0.001);
  //float u0 = 100.0; // giá trị thực (không đổi)
  float u0, e1, e2; // inputs
  float u, u1, u2, u0_new, u1_new; // giá trị đo được (có thêm nhiễu)
  float u_kalman1, u_kalman2; // giá được lọc nhiễu
  float u_temp1, u_temp2;

  ofstream myfile;
  myfile.open ("result.txt");

  for (int i=0; i<2000; i++){
    u0 = rand() % 101 + (-50);// am thanh mong muon [-50 50]
    e1 = rand() % 201 + (-100); // nhieu dien [-100 100]
    e2 = rand() % 21 + (-10);// nhieu am thanh khac [-10 10]
    u1 = u0 + e1; // u0 la cai muon lay ra
    u2 = e2 + u1; // e2 la cai muon lay ra
    //e2 la tin hieu deu` (nhieu nen), kalman se giu lai e2 va loai u1

    // Giu lai dc e2, lay u2 - u_kalman1 se ra "u1'"
    //so sanh u1' voi u1 (theo ly thuyet u1'=u1)
    u_kalman1 = bo_loc.updateEstimate(u2); 
    u_kalman1 = bo_loc.updateEstimate(u_kalman1); 
    u_kalman1 = bo_loc.updateEstimate(u_kalman1); 
    u_kalman1 = bo_loc.updateEstimate(u_kalman1); 

    
    u_kalman1 = bo_loc.updateEstimate(u_kalman1); 
    u_kalman1 = bo_loc.updateEstimate(u_kalman1); 
    u_kalman1 = bo_loc.updateEstimate(u_kalman1); 

    u_kalman1 = bo_loc.updateEstimate(u_kalman1); 
    u_kalman1 = bo_loc.updateEstimate(u_kalman1); 
    u_kalman1 = bo_loc.updateEstimate(u_kalman1); 

    u_kalman1 = bo_loc.updateEstimate(u_kalman1); 
    u_kalman1 = bo_loc.updateEstimate(u_kalman1); 
    u_kalman1 = bo_loc.updateEstimate(u_kalman1); 
    u1_new = u2 - u_kalman1; // nhieu dien + am thanh mong muon

    //loc e1 va giu lai duoc am thanh ban dau
    u0_new = bo_loc2.updateEstimate(u1); 

    //u_kalman = bo_loc.updateEstimate(u_kalman); // tầng 4
    //cout << "u_kalman[" << i << "] = " << u_kalman << endl;
    myfile << u0_new << endl;
  }

  myfile.close();
  return 0;
}
