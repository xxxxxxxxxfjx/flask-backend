from App.models import *
import pandas as pd


def terminalInfo():
    result_t = Terminal.query.all()
    df_res_terminal = pd.DataFrame(
        [(res.smac, res.sip, res.staff, res.staff_group, res.cascadecode, res.domain_id, res.domain_name) for res in
         result_t], columns=['pc', 'ip', 'staff', 'staff_group', 'cascadecode', 'domain_id', 'domain_name'])

    df_res_terminal.to_sql('user-terminal', con=db.engine, if_exists='append', index=False)
