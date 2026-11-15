# Test Cases: React TodoMVC

Target: https://todomvc.com/examples/react/dist/
Reference: [TodoMVC app specification](https://github.com/tastejs/todomvc/blob/master/app-spec.md)

ทุก test เริ่มจากหน้าเว็บใหม่ที่ไม่มีรายการ และ browser context แยกกัน จึงรันลำดับใดหรือรันเดี่ยวก็ได้

| ID | กลุ่ม | Test Title | Expected Result | Priority | Test | สถานะ |
|---|---|---|---|---|---|---|
| TC-TODO-001 | Add | เพิ่ม todo 1 รายการ | รายการแสดง "Buy milk", ตัวนับ "1 item left!", ช่องกรอกว่าง | P1 smoke | `tests/test_add_todo.py` | Automated |
| TC-TODO-002 | Add | เพิ่มหลายรายการ | แสดงครบ 3 รายการตามลำดับที่เพิ่ม, ตัวนับ "3 items left!" | P1 | `tests/test_add_todo.py` | Automated |
| TC-TODO-003 | Add | ข้อความมีช่องว่างหน้าหลัง | บันทึกเป็น "Buy milk" ไม่มีช่องว่าง | P2 | `tests/test_add_todo.py` | Automated |
| TC-TODO-004 | Add | กด Enter ด้วยค่าว่างหรือ space ล้วน (2 data sets) | ไม่มีรายการถูกเพิ่ม, ส่วนรายการยังซ่อน | P2 | `tests/test_add_todo.py` | Automated |
| TC-TODO-005 | Add | ข้อความภาษาไทย, emoji, HTML และ script (3 data sets) | แสดงตรงตามที่พิมพ์ทุกตัวอักษร, HTML ไม่ถูก render | P2 | `tests/test_add_todo.py` | Automated |
| TC-TODO-006 | Add | ข้อความยาว 500 ตัวอักษร | แสดงครบ 500 ตัวอักษร | P3 | `tests/test_add_todo.py` | Automated |
| TC-TODO-007 | Add | ส่วนรายการและ footer เมื่อไม่มีรายการ | ซ่อนตอนว่าง, แสดงหลังเพิ่มรายการแรก | P2 | `tests/test_add_todo.py` | Automated |
| TC-TODO-008 | Complete | ทำเครื่องหมายเสร็จ | รายการมี class `completed`, ตัวนับลดเหลือ "1 item left!" | P1 smoke | `tests/test_complete_todo.py` | Automated |
| TC-TODO-009 | Complete | ยกเลิกเครื่องหมายเสร็จ | class `completed` หายไป, ตัวนับกลับเป็น "2 items left!" | P1 | `tests/test_complete_todo.py` | Automated |
| TC-TODO-010 | Complete | Toggle all ทำเครื่องหมายทุกรายการ | ทุกรายการ `completed`, ตัวนับ "0 items left!" | P1 | `tests/test_complete_todo.py` | Automated |
| TC-TODO-011 | Complete | Toggle all ซ้ำเพื่อยกเลิกทั้งหมด | ไม่มีรายการ `completed`, ตัวนับ "3 items left!" | P2 | `tests/test_complete_todo.py` | Automated |
| TC-TODO-012 | Complete | สถานะ Toggle all ตามรายการ | ติ๊กเมื่อทุกรายการเสร็จ, ไม่ติ๊กเมื่อมีรายการค้าง | P2 | `tests/test_complete_todo.py` | Automated |
| TC-TODO-013 | Edit | แก้ไขแล้วกด Enter | ข้อความเปลี่ยนเป็น "Buy oat milk", ออกจากโหมดแก้ไข | P1 smoke | `tests/test_edit_todo.py` | Automated |
| TC-TODO-014 | Edit | แก้ไขแล้วคลิกที่อื่น (blur) | ข้อความใหม่ถูกบันทึก | P2 | `tests/test_edit_todo.py` | Automated |
| TC-TODO-015 | Edit | แก้เป็นค่าว่างหรือ space ล้วน (2 data sets) | รายการถูกลบ, ตัวนับ "1 item left!" | P2 | `tests/test_edit_todo.py` | Automated |
| TC-TODO-016 | Edit | แก้ไขด้วยข้อความที่มีช่องว่างหน้าหลัง | บันทึกแบบตัดช่องว่าง | P3 | `tests/test_edit_todo.py` | Automated |
| TC-TODO-017 | Edit | กด Escape ระหว่างแก้ไข | ออกจากโหมดแก้ไข และข้อความเดิมไม่เปลี่ยน | P2 | `tests/test_edit_todo.py` | **Known defect** (xfail) |
| TC-TODO-018 | Edit | ระหว่างแก้ไข | ช่องแก้ไขแสดงข้อความเดิม, checkbox และปุ่มลบถูกซ่อน | P3 | `tests/test_edit_todo.py` | Automated |
| TC-TODO-019 | Delete | ลบด้วยปุ่ม × | รายการที่เลือกหายไป ที่เหลือคงลำดับ, ตัวนับ "2 items left!" | P1 smoke | `tests/test_delete_todo.py` | Automated |
| TC-TODO-020 | Counter | คำ item และ items ตามจำนวน (4 data sets) | "1 item left!", "2 items left!", "1 item left!", "0 items left!" | P2 | `tests/test_counter.py` | Automated |
| TC-TODO-021 | Filter | Filter Active | แสดงเฉพาะรายการค้าง, ลิงก์ Active ถูกเลือก, URL ลงท้าย `#/active` | P1 | `tests/test_filter.py` | Automated |
| TC-TODO-022 | Filter | Filter Completed | แสดงเฉพาะรายการเสร็จ, URL ลงท้าย `#/completed` | P1 | `tests/test_filter.py` | Automated |
| TC-TODO-023 | Filter | กลับมา Filter All | แสดงทุกรายการ, ลิงก์ All ถูกเลือก | P2 | `tests/test_filter.py` | Automated |
| TC-TODO-024 | Filter | เปิด URL `#/completed` โดยตรง | ลิงก์ Completed ถูกเลือก, รายการใหม่ไม่แสดงใน view นี้แต่ตัวนับอัปเดต | P2 | `tests/test_filter.py` | Automated |
| TC-TODO-025 | Filter | ปุ่ม Back ของ browser | กลับไป filter ก่อนหน้าพร้อมรายการที่ถูกต้อง | P3 | `tests/test_filter.py` | Automated |
| TC-TODO-026 | Filter | ทำเครื่องหมายเสร็จขณะอยู่ใน Active | รายการหายจาก view ทันที, ตัวนับลดลง | P2 | `tests/test_filter.py` | Automated |
| TC-TODO-027 | Clear | Clear completed | ลบเฉพาะรายการที่เสร็จ, ปุ่มหายไป | P1 | `tests/test_clear_completed.py` | Automated |
| TC-TODO-028 | Clear | การแสดงปุ่ม Clear completed | ซ่อนเมื่อไม่มีรายการเสร็จ, แสดงเมื่อมีอย่างน้อย 1 รายการ | P2 | `tests/test_clear_completed.py` | Automated |
| TC-TODO-029 | Persistence | Refresh หน้าเว็บ | รายการและสถานะยังอยู่ครบ | P2 | `tests/test_persistence.py` | **Known defect** (xfail) |
| TC-TODO-030 | Journey | เพิ่ม, ทำเครื่องหมาย, แก้ไข, filter, clear ครบ flow | ทุกขั้นตอนแสดงผลถูกต้องต่อเนื่อง | P1 smoke | `tests/test_user_journey.py` | Automated |

รวม 30 TC เป็น 37 test เพราะ TC-004, 005, 015 และ 020 เป็น data-driven

## Known defects

| TC | Spec | สิ่งที่เกิดจริงบนเว็บ | ผลกระทบ |
|---|---|---|---|
| TC-TODO-017 | กด Escape ต้องยกเลิกการแก้ไขและคืนข้อความเดิม | ยังอยู่ในโหมดแก้ไข และเมื่อคลิกที่อื่น ข้อความที่พิมพ์ไว้ถูกบันทึกทับ | ผู้ใช้ที่ตั้งใจยกเลิกเสียข้อความเดิม |
| TC-TODO-029 | ต้องเก็บรายการใน localStorage | เก็บใน memory อย่างเดียว refresh แล้วรายการหายทั้งหมด | ข้อมูลผู้ใช้หายทุกครั้งที่ปิดหรือ refresh |

## Out of scope

- Visual และ layout: ตรวจด้วยตาได้ดีกว่า automate
- Accessibility แบบเต็ม: ควรใช้เครื่องมือเฉพาะ เช่น axe-core เป็นชุดแยก
- Performance: TodoMVC ทำงานฝั่ง browser ทั้งหมด ไม่มี backend
