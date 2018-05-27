*** Settings ***

Library    OperatingSystem
Library    Collections

Library    ./lib/helpers.py


*** Keywords ***

Assert ${path} Returns ${code}
    ${retval}=    Make Request For Status Code    ${path}
    ${code_as_int}=    Convert To Integer    ${code}
    Should Be Equal    ${retval}   ${code_as_int}

Assert ${path} Contains ${sub_dict}
    ${retval}=    Make Request For Response    ${path}
    Dictionary Should Contain Sub Dictionary    ${retval}    ${sub_dict}