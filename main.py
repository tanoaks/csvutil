import os
import csv
import json

state_data = {}
ref_dict = {}


def get_value(row, data):
    return row[ref_dict.get(data)]


def rule_create_bp(row):
    bp = float(get_value(row, 'z')) + float(get_value(row, 'ab')) + float(get_value(row, 'ad'))
    row[ref_dict.get('bp')] = bp
    return ''


def rule_bp_equal_au(row, log):
    bp = float(get_value(row, 'bp'))
    au = float(get_value(row, 'au'))
    if au != bp:
        log = log + 'error row BP not equal AU'
    return log


def rule_au_zero_al(row, log):
    au = float(get_value(row, 'au'))
    al = float(get_value(row, 'al'))
    if (au == 0) and (al != 0):
        log = log + ' :error row AU zero equal AU but AL not zero'
    return log


def rule_state_code_bl(row, log):
    gst_tin = str(get_value(row, 'c')).strip()
    state_code = int(gst_tin[0:2])
    row[ref_dict.get('bl')] = state_data[str(state_code)]
    return log


def rule_bl_not_equal_q(row, log):
    q = str(get_value(row, 'q')).strip()
    bl = str(get_value(row, 'bl')).strip()
    if q.lower() != bl.lower():
        log = log + ' :error row BL not equal Q'
    return log


def rule_k_equal_invoice_and_bl_not_aq_then_ai_ak_bg_bh_zero_and_ag_bf_greater_zero(row, log):
    k = str(get_value(row, 'k')).strip()
    bl = str(get_value(row, 'bl')).strip()
    aq = str(get_value(row, 'aq')).strip()
    ai = float(get_value(row, 'ai'))
    ak = float(get_value(row, 'ak'))
    bg = float(get_value(row, 'bg'))
    bh = float(get_value(row, 'bh'))
    ag = float(get_value(row, 'ag'))
    bf = float(get_value(row, 'bf'))
    if k.lower() == 'invoice' and bl != aq:
        if ai == 0.0 and ak == 0.0 and bg == 0.0 and bh == 0.0 and ag > 0.0 and bf > 0.0:
            pass
        else:
            log = log + '  :invoice error k_equal_invoice_and_bl_not_aq_then_ai_ak_bg_bh_zero_and_ag_bf_greater_zero'
    return log


def rule_k_equal_invoice_and_bl_eq_aq_then_ai_ak_bg_bh_greater_zero(row, log):
    k = str(get_value(row, 'k')).strip()
    bl = str(get_value(row, 'bl')).strip()
    aq = str(get_value(row, 'aq')).strip()
    ai = float(get_value(row, 'ai'))
    ak = float(get_value(row, 'ak'))
    bg = float(get_value(row, 'bg'))
    bh = float(get_value(row, 'bh'))
    ag = float(get_value(row, 'ag'))
    bf = float(get_value(row, 'bf'))
    if k.lower() == 'invoice' and bl == aq:
        if ai > 0.0 and ak > 0.0 and bg > 0.0 and bh > 0.0 and ag == 0.0 and bf == 0.0:
            pass
        else:
            log = log + '  :invoice error k_equal_invoice_and_bl_eq_aq_then_ai_ak_bg_bh_greater_zero'
    return log


def rule_column_k_invoice_then_set_bs_bt_bv_bw_bx(row, log):
    k = str(get_value(row, 'k')).strip()
    if k.lower() == 'invoice':
        row[ref_dict.get('bs')] = str(get_value(row, 'bc')).strip()
        row[ref_dict.get('bt')] = str(get_value(row, 'bd')).strip()
        row[ref_dict.get('bv')] = str(get_value(row, 'ag')).strip()
        row[ref_dict.get('bw')] = str(get_value(row, 'ai')).strip()
        row[ref_dict.get('bx')] = str(get_value(row, 'ak')).strip()
    return log


def rule_column_k_credit_note_then_set_bu(row, log):
    k = str(get_value(row, 'k')).strip()
    if k.lower() == 'credit note':
        row[ref_dict.get('bu')] = str(get_value(row, 'bd')).strip()
    return log


def apply_rule(file_read, write_file):
    print(file_read)
    csvreader = csv.reader(file_read)
    header = next(csvreader)
    header.append('errors')
    csvwriter = csv.writer(write_file)
    csvwriter.writerow(header)
    log = ''
    for row in csvreader:
        try:
            log = rule_create_bp(row)
        except Exception as inst:
            print('exp1')
        try:
            log = rule_bp_equal_au(row, log)
        except Exception as inst:
            print('exp2')
        try:
            log = rule_au_zero_al(row, log)
        except Exception as inst:
            print('exp3')
        try:
            log = rule_state_code_bl(row, log)
        except Exception as inst:
            print('exp4')
        try:
            log = rule_bl_not_equal_q(row, log)
        except Exception as inst:
            print('exp5')
        try:
            log = rule_k_equal_invoice_and_bl_not_aq_then_ai_ak_bg_bh_zero_and_ag_bf_greater_zero(row, log)
        except Exception as inst:
            print('exp6')
        try:
            log = rule_column_k_invoice_then_set_bs_bt_bv_bw_bx(row, log)
        except Exception as inst:
            print('excp7')
        try:
            log = rule_column_k_credit_note_then_set_bu(row, log)
        except Exception as inst:
            print('exp8')
        try:
            log = rule_k_equal_invoice_and_bl_eq_aq_then_ai_ak_bg_bh_greater_zero(row, log)
        except Exception as inst:
            print('exp8')
         
        row.append(log)
        csvwriter.writerow(row)

    write_file.close()
    file_read.close()


def main():
    directory = os.getcwd()
    dpath = os.path.join(directory, 'data')
    o_path = os.path.join(directory, 'out')
    all_file = os.listdir(dpath)
    for file in all_file:
        file_data = open(os.path.join(dpath, file), encoding='utf-8')
        write_file = open(os.path.join(o_path, file), 'w', newline='' , encoding='utf-8')
        apply_rule(file_data, write_file)


def create_array():
    ref_abc = []
    for i in range(0, 26):
        ref_abc.append(chr(i + ord('a')))
    for i in range(0, 67):
        ref_abc.append(str(ref_abc[(i // 26)] + ref_abc[(i % 26)]))
    print(ref_abc)
    for i in range(0, len(ref_abc)):
        ref_dict.update({ref_abc[i]: i})
    return ref_dict


if __name__ == '__main__':
    ref_dict = create_array()
    state_file = os.path.join(os.getcwd(), 'stateist')
    with open(state_file) as json_file:
        state_data = json.load(json_file)
    main()
