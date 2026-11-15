# TodoMVC React: UI Automation Tests

ชุด automation test สำหรับ [React TodoMVC](https://todomvc.com/examples/react/dist/) เขียนด้วย **Python + Pytest + Playwright**

- 30 Test Cases (37 test เมื่อรวม data-driven) ครอบคลุมการเพิ่ม, ทำเครื่องหมายเสร็จ, แก้ไข, ลบ, ตัวนับ, filter, clear completed, การเก็บข้อมูล และ user journey
- พบ defect 2 ข้อที่ไม่ตรงกับ [TodoMVC spec](https://github.com/tastejs/todomvc/blob/master/app-spec.md) ดูหัวข้อ [Known defects](#known-defects)
- รายละเอียด Test Cases ทั้งหมดอยู่ที่ [`docs/test-cases.md`](docs/test-cases.md)

ผลรันล่าสุดบน Chromium: `35 passed, 2 xfailed` (2 xfailed คือ known defect ที่ตั้งใจให้แสดงในรายงาน)

---

## 1. สิ่งที่ต้องมีในเครื่อง

| โปรแกรม | Version | ตรวจสอบด้วยคำสั่ง |
|---|---|---|
| Python | 3.10 ขึ้นไป | `python --version` (macOS/Linux อาจเป็น `python3 --version`) |
| Git | version ใดก็ได้ | `git --version` |

ถ้ายังไม่มี Python ดาวน์โหลดได้ที่ https://www.python.org/downloads/ บน Windows ตอนติดตั้งให้ติ๊ก **"Add python.exe to PATH"**

## 2. ติดตั้ง

### 2.1 Clone repo

```bash
git clone <URL ของ repo นี้>
cd todomvc-automation
```

### 2.2 สร้าง virtual environment

แยก library ของโปรเจกต์นี้ออกจาก Python หลักของเครื่อง

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

ถ้า PowerShell แจ้งว่ารัน script ไม่ได้ ให้รันคำสั่งนี้ครั้งเดียวแล้ว activate ใหม่:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

**Windows (Command Prompt)**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

เมื่อ activate สำเร็จ จะเห็น `(.venv)` นำหน้าบรรทัดคำสั่ง

### 2.3 ติดตั้ง library และ browser

```bash
pip install -r requirements.txt
playwright install
```

`playwright install` ดาวน์โหลด Chromium, Firefox และ WebKit ที่ Playwright ใช้ (ประมาณ 500 MB ครั้งแรกครั้งเดียว) ถ้าต้องการแค่ Chromium ใช้ `playwright install chromium`

บน Linux ถ้ามี error เรื่อง library ของระบบ ใช้ `playwright install --with-deps`

| Library | ใช้ทำอะไร |
|---|---|
| `playwright` | ควบคุม browser และรอ element อัตโนมัติ |
| `pytest` | test runner |
| `pytest-playwright` | เชื่อม Playwright กับ pytest: fixture `page`, เลือก browser, screenshot และ trace เมื่อ fail |
| `pytest-html` | สร้างรายงาน HTML |

## 3. รัน test

```bash
pytest
```

รันกับเว็บจริงบน Chromium แบบ headless (ไม่เปิดหน้าต่าง) ใช้เวลาประมาณ 40 วินาที

| ต้องการ | คำสั่ง |
|---|---|
| เห็น browser ขณะรัน | `pytest --headed --slowmo 300` |
| เลือก browser | `pytest --browser firefox` หรือ `--browser webkit` |
| รันทั้ง 3 browser | `pytest --browser chromium --browser firefox --browser webkit` |
| เฉพาะ smoke test | `pytest -m smoke` |
| เฉพาะ P1 | `pytest -m P1` |
| ข้าม known defect | `pytest -m "not known_defect"` |
| รัน TC เดียว | `pytest -k TC_TODO_013` |
| ดูชื่อ test แบบละเอียด | `pytest -v` |
| รันกับเว็บอื่น เช่น copy ในเครื่อง | `pytest --base-url http://localhost:8080/` |

## 4. ดูผล

- **รายงาน HTML:** `reports/report.html` เปิดด้วย browser ได้เลย
- **เมื่อ test fail:** screenshot และ trace เก็บอยู่ใน `test-results/<ชื่อ test>/`
- **เปิด trace:** แสดงทุกขั้นตอน, DOM, network และ console ย้อนดูได้ทีละ action

```bash
playwright show-trace test-results/<ชื่อ test>/trace.zip
```

ผลในบรรทัดสุดท้ายของ pytest อ่านแบบนี้:

| ผล | ความหมาย |
|---|---|
| `passed` | ทำงานตาม Expected Result |
| `xfailed` | known defect ยังเกิดอยู่ตามที่บันทึกไว้ ไม่ถือว่า suite ล้ม |
| `failed` | พบ regression หรือ test ต้องแก้ ดูรายงานและ trace |
| `XPASS(strict)` แสดงเป็น failed | known defect ถูกแก้แล้ว ให้ลบ `xfail` ออกจาก test นั้น |

## 5. โครงสร้าง

```
todomvc-automation/
├── README.md
├── requirements.txt          # version ตายตัว ทุกเครื่องได้ผลเหมือนกัน
├── pytest.ini                # base URL, markers, รายงาน, screenshot และ trace เมื่อ fail
├── conftest.py               # fixture todo_page: เปิดหน้าเว็บใหม่ให้ทุก test
├── pages/
│   └── todo_page.py          # Page Object: locator และ action เท่านั้น
├── test_data/
│   └── todos.py              # ข้อมูลทดสอบและข้อความที่ต้องตรวจ
├── tests/                    # 1 ไฟล์ต่อ 1 feature, ชื่อ test ขึ้นต้นด้วย TC ID
│   ├── test_add_todo.py
│   ├── test_complete_todo.py
│   ├── test_edit_todo.py
│   ├── test_delete_todo.py
│   ├── test_counter.py
│   ├── test_filter.py
│   ├── test_clear_completed.py
│   ├── test_persistence.py
│   └── test_user_journey.py
├── docs/
│   └── test-cases.md         # Test Cases ทั้งหมด และ mapping กับไฟล์ test
└── .github/workflows/
    └── tests.yml             # รันอัตโนมัติบน GitHub Actions ทั้ง 3 browser
```

## 6. แนวทางการออกแบบ

**Page Object Model:** locator และ action ของหน้าเว็บอยู่ใน `pages/todo_page.py` ที่เดียว ถ้าหน้าเว็บเปลี่ยน แก้ไฟล์เดียว test ไม่ต้องแก้ Page Object ไม่มี assertion เพื่อให้ test อ่านแล้วเห็นว่าตรวจอะไร

**Locator:** ใช้ role และ accessible name ก่อน (เช่น `get_by_role("button", name="Clear completed")`) รองลงมาคือ `data-testid` ที่แอปมีให้ ไม่ใช้ XPath หรือลำดับ element ซึ่งพังง่ายเมื่อหน้าเว็บเปลี่ยน locator ทุกตัวตรวจกับเว็บจริงแล้ว

**ไม่มี sleep:** ใช้ `expect(...)` ของ Playwright ที่รอจนเงื่อนไขเป็นจริงเอง test จึงไม่ช้าโดยไม่จำเป็นและไม่ flaky จากจังหวะเวลา

**Test อิสระต่อกัน:** ทุก test ได้ browser context ใหม่และเริ่มจากรายการว่าง สร้างข้อมูลของตัวเอง รันลำดับใด รันเดี่ยว หรือรันขนานก็ได้

**Data-driven:** ข้อมูลทดสอบแยกไว้ใน `test_data/todos.py` เพิ่ม data set ได้โดยไม่แตะ logic ของ test

**Known defect ใช้ `xfail(strict=True, raises=AssertionError)`:**
- suite ยังผ่าน ทีมไม่ชินกับการเห็น test แดงตลอดเวลา
- รายงานแสดง defect ชัดเจนพร้อมเหตุผล
- ถ้าแอปแก้แล้ว test จะ fail เตือนให้ลบ `xfail` ออก
- `raises=AssertionError` ทำให้ error อื่น เช่น เว็บล่มหรือ locator เสีย ไม่ถูกซ่อนเป็น xfail

**Traceability:** ชื่อ test ขึ้นต้นด้วย TC ID ตรงกับ `docs/test-cases.md` และติด marker `smoke`, `P1` ถึง `P3` เพื่อเลือกชุดที่รันได้

## Known defects

| TC | Spec กำหนด | ที่เกิดจริง |
|---|---|---|
| TC-TODO-017 | กด Escape ระหว่างแก้ไขต้องยกเลิกและคืนข้อความเดิม | ยังอยู่ในโหมดแก้ไข และเมื่อคลิกที่อื่น ข้อความที่พิมพ์ไว้ถูกบันทึกทับของเดิม |
| TC-TODO-029 | รายการต้องถูกเก็บใน localStorage | refresh แล้วรายการหายทั้งหมด |

## 7. CI

`.github/workflows/tests.yml` รัน test อัตโนมัติทุกครั้งที่ push หรือเปิด pull request บน Chromium, Firefox และ WebKit แบบขนาน รายงานและไฟล์ trace ของ test ที่ fail ดาวน์โหลดได้จากหน้า Actions ของแต่ละรอบ

## 8. แก้ปัญหาที่พบบ่อย

| อาการ | วิธีแก้ |
|---|---|
| `playwright: command not found` | ยังไม่ได้ activate virtual environment ดูข้อ 2.2 |
| `Executable doesn't exist ... ms-playwright` | ยังไม่ได้ติดตั้ง browser รัน `playwright install` |
| `ModuleNotFoundError: No module named 'pages'` | ต้องรัน `pytest` จากโฟลเดอร์ `todomvc-automation` |
| test ช้าหรือ timeout ทั้งชุด | ตรวจว่าเปิด https://todomvc.com/examples/react/dist/ ใน browser ได้ |
