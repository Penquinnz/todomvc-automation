# TodoMVC React: UI Automation Tests

ชุด automation test สำหรับ [React TodoMVC](https://todomvc.com/examples/react/dist/) เขียนด้วย **Python + Pytest + Playwright**

- 30 Test Cases (37 test เมื่อรวม data-driven) ครอบคลุมการเพิ่ม, ทำเครื่องหมายเสร็จ, แก้ไข, ลบ, ตัวนับ, filter, clear completed, การเก็บข้อมูล และ user journey
- พบ defect 2 ข้อที่ไม่ตรงกับ [TodoMVC spec](https://github.com/tastejs/todomvc/blob/master/app-spec.md) ดูหัวข้อ [Known defects](#known-defects)
- รายละเอียด Test Cases ทั้งหมดอยู่ที่ [`docs/test-cases.md`](docs/test-cases.md)

ผลรันล่าสุดบน Chromium: `35 passed, 2 xfailed` (2 xfailed คือ known defect ที่ตั้งใจให้แสดงในรายงาน)

---

## 1. สิ่งที่ต้องมีในเครื่อง

| โปรแกรม | Version |
|---|---|
| Python | **3.10 ขึ้นไป** (แนะนำ 3.12) |
| Git | version ใดก็ได้ |

ถ้า Python ต่ำกว่า 3.10 จะติดตั้ง library ไม่ได้ (pip แจ้งว่าหา `playwright==1.63.0` ไม่เจอ) ขั้นตอนในข้อ 2 รวมการเช็กและติดตั้ง Python 3.12 ไว้แล้ว ไม่ต้องลบ Python ตัวเดิม

| Library ที่ติดตั้งจาก `requirements.txt` | ใช้ทำอะไร |
|---|---|
| `playwright` | ควบคุม browser และรอ element อัตโนมัติ |
| `pytest` | test runner |
| `pytest-playwright` | เชื่อม Playwright กับ pytest: fixture `page`, เลือก browser, screenshot และ trace เมื่อ fail |
| `pytest-html` | สร้างรายงาน HTML |

## 2. ติดตั้งและรันครั้งแรก

เลือกตามระบบปฏิบัติการ ทำครั้งเดียวต่อเครื่อง

### 2A. Windows (PowerShell)

**ขั้นที่ 1 เช็ก Python**

```powershell
py -0
```

คำสั่งนี้แสดง Python ทุก version ในเครื่อง ถ้าในรายการมี 3.10 ขึ้นไป ข้ามไปขั้นที่ 2 ถ้าไม่มี หรือขึ้นว่าไม่รู้จักคำสั่ง `py` ให้ติดตั้ง Python 3.12:

```powershell
winget install Python.Python.3.12
```

ถ้าค้างที่ "Starting package install" ให้ดูที่ taskbar ว่ามีหน้าต่างขออนุญาตรอให้กด Yes อยู่หรือไม่ หรือดาวน์โหลดจาก https://www.python.org/downloads/ แล้วติ๊ก **"Add python.exe to PATH"** ตอนติดตั้ง จากนั้นปิดและเปิด Terminal ใหม่

**ขั้นที่ 2 Clone repo**

```powershell
git clone <URL ของ repo นี้>
cd todomvc-automation
```

**ขั้นที่ 3 สร้างและ activate virtual environment**

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python --version
```

บรรทัดสุดท้ายต้องขึ้น `Python 3.12.x` และบรรทัดคำสั่งต้องมี `(.venv)` นำหน้า ถ้าใช้ Python version อื่นที่ 3.10 ขึ้นไป เปลี่ยน `-3.12` เป็น version นั้น

ถ้าขึ้นว่า "running scripts is disabled on this system" ให้รันคำสั่งนี้ครั้งเดียว ตอบ `Y` แล้ว activate ใหม่:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

ถ้าใช้ Command Prompt แทน PowerShell ให้ activate ด้วย `.venv\Scripts\activate.bat`

**ขั้นที่ 4 ติดตั้ง library และ browser**

```powershell
pip install -r requirements.txt
playwright install
```

`playwright install` ดาวน์โหลด Chromium, Firefox และ WebKit (ประมาณ 500 MB ครั้งแรกครั้งเดียว)

**ขั้นที่ 5 รัน**

```powershell
python -m pytest --browser chromium --browser firefox --browser webkit
```

ผลที่ควรได้: `105 passed, 6 xfailed`

### 2B. macOS (Terminal)

**ขั้นที่ 1 เช็ก Python**

```bash
python3 --version
```

Mac ส่วนใหญ่มี Python 3.9 มากับ Command Line Tools ของ Apple ซึ่งใช้ไม่ได้ ให้ติดตั้ง Python 3.12 เพิ่ม:

```bash
brew install python@3.12
```

ถ้ายังไม่มี Homebrew ดาวน์โหลด Python 3.12 จาก https://www.python.org/downloads/macos/ แทนได้ ทั้งสองทางจะได้คำสั่ง `python3.12` มาใช้

ครั้งแรกที่ใช้ `git` หรือ `brew` บน Mac อาจมีหน้าต่างให้ติดตั้ง Command Line Tools ให้กด Install แล้วรอจนเสร็จ

**ขั้นที่ 2 Clone repo**

```bash
git clone <URL ของ repo นี้>
cd todomvc-automation
```

**ขั้นที่ 3 สร้างและ activate virtual environment**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python --version
```

ใช้ `python3.12` ตรงๆ ไม่ใช้ `python3` เพราะ `python3` อาจชี้ไปที่ 3.9 ของ Apple บรรทัดสุดท้ายต้องขึ้น `Python 3.12.x` และบรรทัดคำสั่งต้องมี `(.venv)` นำหน้า

**ขั้นที่ 4 ติดตั้ง library และ browser**

```bash
pip install -r requirements.txt
playwright install
```

**ขั้นที่ 5 รัน**

```bash
python -m pytest --browser chromium --browser firefox --browser webkit
```

ผลที่ควรได้: `105 passed, 6 xfailed` บน Mac ผลของ WebKit ใกล้เคียง Safari จริงมากที่สุด

### 2C. Linux

ทำเหมือน macOS โดยติดตั้ง Python 3.12 จาก package manager ของ distro และใช้ `playwright install --with-deps` ในขั้นที่ 4 เพื่อติดตั้ง library ของระบบที่ browser ต้องใช้

### เปิด Terminal ครั้งต่อไป

ไม่ต้องติดตั้งซ้ำ แค่เข้าโฟลเดอร์แล้ว activate ก่อนรัน:

- Windows: `.venv\Scripts\Activate.ps1`
- macOS และ Linux: `source .venv/bin/activate`

## 3. รัน test

```bash
python -m pytest
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

คำสั่งในตารางข้างบนใช้ `pytest` สั้นๆ ได้เมื่อ activate virtual environment แล้ว ถ้า Terminal หาคำสั่งไม่เจอ ให้ใช้ `python -m pytest` แทน

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
| `No matching distribution found for playwright==1.63.0` | Python ต่ำกว่า 3.10 ติดตั้ง Python 3.12 แล้วสร้าง venv ใหม่ ดูข้อ 2A หรือ 2B ขั้นที่ 1 และ 3 |
| `pytest : The term 'pytest' is not recognized` | ยังไม่ได้ activate virtual environment (ดูข้อ 2 ขั้นที่ 3) หรือใช้ `python -m pytest` แทน |
| `running scripts is disabled on this system` | รัน `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` ครั้งเดียว แล้ว activate ใหม่ |
| `playwright: command not found` | ยังไม่ได้ activate virtual environment ดูข้อ 2 ขั้นที่ 3 |
| `Executable doesn't exist ... ms-playwright` | ยังไม่ได้ติดตั้ง browser รัน `playwright install` |
| macOS: `python3 -m venv` ได้ Python 3.9 | ใช้ `python3.12 -m venv .venv` แทน ดูข้อ 2B ขั้นที่ 3 |
| `ModuleNotFoundError: No module named 'pages'` | ต้องรัน `pytest` จากโฟลเดอร์ `todomvc-automation` |
| test ช้าหรือ timeout ทั้งชุด | ตรวจว่าเปิด https://todomvc.com/examples/react/dist/ ใน browser ได้ |
