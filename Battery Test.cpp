#include <iostream>
#include <windows.h>

using namespace std;

int main() {
    //Refer http://msdn.microsoft.com/en-us/library/windows/desktop/aa373232%28v=vs.85%29.aspx
    SYSTEM_POWER_STATUS spsPwr;
    if( GetSystemPowerStatus(&spsPwr) ) {
        cout << static_cast<double>(spsPwr.ACLineStatus) << " "
             << static_cast<double>(spsPwr.BatteryLifePercent) << endl;
        return 0;
    } else return 1;
}
