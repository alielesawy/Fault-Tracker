# دليل المستخدم - نظام إدارة أعطال الأجهزة الطبية
# User Guide - Medical Device Fault Management System

## المحتويات / Contents

1. [مقدمة / Introduction](#مقدمة--introduction)
2. [بدء الاستخدام / Getting Started](#بدء-الاستخدام--getting-started)
3. [الإبلاغ عن عطل / Reporting a Fault](#الإبلاغ-عن-عطل--reporting-a-fault)
4. [إدارة الأعطال (للفنيين) / Managing Faults (Technicians)](#إدارة-الأعطال-للفنيين--managing-faults-technicians)
5. [لوحة تحكم المشرف / Admin Dashboard](#لوحة-تحكم-المشرف--admin-dashboard)
6. [إدارة الأجهزة / Device Management](#إدارة-الأجهزة--device-management)
7. [إعدادات الحساب / Account Settings](#إعدادات-الحساب--account-settings)
8. [تغيير اللغة / Changing Language](#تغيير-اللغة--changing-language)
9. [المساعدة / Help](#المساعدة--help)

## مقدمة / Introduction

نظام إدارة أعطال الأجهزة الطبية هو تطبيق ويب مصمم لتبسيط عملية الإبلاغ عن أعطال الأجهزة الطبية ومتابعتها وإصلاحها في المنشآت الصحية. يدعم التطبيق اللغتين العربية والإنجليزية ويوفر واجهة سهلة الاستخدام للمستخدمين العاديين والفنيين والمشرفين.

The Medical Device Fault Management System is a web application designed to streamline the process of reporting, tracking, and resolving medical device faults in healthcare facilities. The application supports both Arabic and English languages and provides an easy-to-use interface for general users, technicians, and administrators.

## بدء الاستخدام / Getting Started

### تسجيل الدخول / Login

1. انتقل إلى صفحة تسجيل الدخول عن طريق النقر على "تسجيل الدخول" في الشريط العلوي.
2. أدخل البريد الإلكتروني وكلمة المرور.
3. انقر على "تسجيل الدخول".

---

1. Navigate to the login page by clicking "Login" in the top navigation bar.
2. Enter your email and password.
3. Click "Sign In".

### حسابات المستخدمين / User Accounts

النظام يحتوي على ثلاثة أنواع من المستخدمين:

1. **المستخدم العام**: يمكن للمستخدمين العاديين (غير المسجلين) الإبلاغ عن أعطال الأجهزة فقط.
2. **الفني**: يمكن للفنيين عرض تقارير الأعطال والرد عليها وإدارة الأجهزة.
3. **المشرف**: لديه وصول كامل لجميع وظائف النظام، بما في ذلك إدارة المستخدمين والوحدات والتقارير.

---

The system has three types of users:

1. **General User**: Non-logged in users can only report device faults.
2. **Technician**: Technicians can view fault reports, respond to them, and manage devices.
3. **Admin**: Has full access to all system functions, including user, unit, and report management.

## الإبلاغ عن عطل / Reporting a Fault

لا يلزم تسجيل الدخول للإبلاغ عن عطل. هذه الميزة متاحة للعامة:

1. انتقل إلى الصفحة الرئيسية.
2. انقر على "الإبلاغ عن عطل".
3. املأ النموذج بالمعلومات المطلوبة:
   - اسم الجهاز
   - الرقم التسلسلي (اختياري)
   - الوحدة/القسم
   - وصف العطل
4. انقر على "إرسال".
5. سيتلقى الفنيون إشعارًا بالتقرير الجديد.

---

You don't need to be logged in to report a fault. This feature is available to the public:

1. Go to the home page.
2. Click on "Report a Fault".
3. Fill in the form with the required information:
   - Device name
   - Serial number (optional)
   - Unit/Department
   - Fault description
4. Click "Submit".
5. Technicians will receive notification of the new report.

## إدارة الأعطال (للفنيين) / Managing Faults (Technicians)

### عرض تقارير الأعطال / Viewing Fault Reports

1. قم بتسجيل الدخول كفني أو مشرف.
2. انتقل إلى "تقارير الأعطال" في القائمة.
3. اطلع على قائمة بجميع تقارير الأعطال مع حالتها.
4. استخدم خيارات الترشيح والبحث للعثور على تقارير محددة.

---

1. Log in as a technician or admin.
2. Navigate to "Fault Reports" in the menu.
3. View a list of all fault reports with their status.
4. Use filtering and search options to find specific reports.

### الرد على تقرير عطل / Responding to a Fault Report

1. انقر على تقرير عطل في القائمة لعرض التفاصيل.
2. اقرأ وصف العطل ومعلومات الجهاز.
3. أدخل الإجراء المتخذ في حقل الاستجابة.
4. انقر على "إرسال الرد" لتحديث التقرير وتغيير حالته إلى "تم الحل".

---

1. Click on a fault report in the list to view details.
2. Read the fault description and device information.
3. Enter the action taken in the response field.
4. Click "Submit Response" to update the report and change its status to "Resolved".

## لوحة تحكم المشرف / Admin Dashboard

### الوصول إلى لوحة التحكم / Accessing the Dashboard

1. قم بتسجيل الدخول كمشرف.
2. انتقل إلى "لوحة التحكم" في القائمة.
3. اطلع على لوحة التحكم التي تعرض إحصاءات وبيانات حول:
   - إجمالي عدد الأجهزة
   - الأجهزة العاملة/المعطلة
   - تقارير الأعطال المعلقة/المحلولة
   - إحصاءات حسب الوحدة وفئة الجهاز

---

1. Log in as an admin.
2. Navigate to "Dashboard" in the menu.
3. View the dashboard displaying statistics and data about:
   - Total devices
   - Working/faulty devices
   - Pending/resolved fault reports
   - Statistics by unit and device category

### إدارة المستخدمين / User Management

1. انتقل إلى "إدارة المستخدمين" في قائمة المشرف.
2. اطلع على قائمة بجميع المستخدمين.
3. انقر على "إضافة مستخدم" لإنشاء حساب مستخدم جديد.
4. حرر معلومات المستخدم أو احذف المستخدمين حسب الحاجة.

---

1. Navigate to "User Management" in the admin menu.
2. View a list of all users.
3. Click "Add User" to create a new user account.
4. Edit user information or delete users as needed.

### إدارة الوحدات / Unit Management

1. انتقل إلى "إدارة الوحدات" في قائمة المشرف.
2. اطلع على قائمة بجميع الوحدات (الأقسام).
3. انقر على "إضافة وحدة" لإضافة وحدة جديدة.
4. حرر معلومات الوحدة أو احذف الوحدات حسب الحاجة.

---

1. Navigate to "Unit Management" in the admin menu.
2. View a list of all units (departments).
3. Click "Add Unit" to add a new unit.
4. Edit unit information or delete units as needed.

### التقارير / Reports

1. انتقل إلى "التقارير" في قائمة المشرف.
2. اختر نوع التقرير (تقارير الأعطال أو مخزون الأجهزة).
3. حدد نطاق التاريخ (اختياري).
4. انقر على "إنشاء التقرير" لعرض البيانات.

---

1. Navigate to "Reports" in the admin menu.
2. Choose the report type (fault reports or device inventory).
3. Set the date range (optional).
4. Click "Generate Report" to view the data.

## إدارة الأجهزة / Device Management

### عرض الأجهزة / Viewing Devices

1. قم بتسجيل الدخول كفني أو مشرف.
2. انتقل إلى "قائمة الأجهزة" في القائمة.
3. استعرض قائمة بجميع الأجهزة المسجلة مع معلوماتها.

---

1. Log in as a technician or admin.
2. Navigate to "Device List" in the menu.
3. Browse a list of all registered devices with their information.

### إضافة جهاز جديد / Adding a New Device

1. انتقل إلى "قائمة الأجهزة".
2. انقر على "إضافة جهاز".
3. املأ النموذج بالمعلومات المطلوبة:
   - الرقم التسلسلي
   - اسم الجهاز
   - نوع الجهاز
   - الموديل
   - الوحدة
   - الفئة
   - بلد المنشأ
   - الحالة
   - الوصف
4. انقر على "حفظ الجهاز".

---

1. Navigate to "Device List".
2. Click "Add Device".
3. Fill in the form with the required information:
   - Serial number
   - Device name
   - Device type
   - Model
   - Unit
   - Category
   - Origin country
   - Status
   - Description
4. Click "Save Device".

### تعديل معلومات الجهاز / Editing Device Information

1. انتقل إلى "قائمة الأجهزة".
2. ابحث عن الجهاز المطلوب تعديله.
3. انقر على زر "تعديل" بجانب الجهاز.
4. قم بتحديث المعلومات حسب الحاجة.
5. انقر على "حفظ الجهاز" للحفظ.

---

1. Navigate to "Device List".
2. Find the device you want to edit.
3. Click the "Edit" button next to the device.
4. Update the information as needed.
5. Click "Save Device" to save.

## إعدادات الحساب / Account Settings

### تعديل الملف الشخصي / Editing Your Profile

1. قم بتسجيل الدخول إلى حسابك.
2. انقر على اسم المستخدم في الشريط العلوي.
3. اختر "الملف الشخصي".
4. قم بتحديث معلوماتك الشخصية.
5. انقر على "تحديث الملف الشخصي" للحفظ.

---

1. Log in to your account.
2. Click on your username in the top bar.
3. Select "Profile".
4. Update your personal information.
5. Click "Update Profile" to save.

### إعادة تعيين كلمة المرور / Resetting Your Password

1. في صفحة تسجيل الدخول، انقر على "نسيت كلمة المرور".
2. أدخل عنوان بريدك الإلكتروني.
3. انقر على "طلب إعادة تعيين كلمة المرور".
4. ستتلقى رسالة بريد إلكتروني مع رابط لإعادة تعيين كلمة المرور.
5. اتبع الرابط وأدخل كلمة مرور جديدة.

---

1. On the login page, click "Forgot Password".
2. Enter your email address.
3. Click "Request Password Reset".
4. You'll receive an email with a link to reset your password.
5. Follow the link and enter a new password.

## تغيير اللغة / Changing Language

1. انقر على زر تبديل اللغة في الشريط العلوي (العربية/English).
2. ستتغير واجهة المستخدم إلى اللغة المحددة على الفور.
3. يتم حفظ تفضيل اللغة في الجلسة لزياراتك القادمة.

---

1. Click the language toggle button in the top bar (Arabic/English).
2. The user interface will immediately change to the selected language.
3. Your language preference is saved in the session for your future visits.

## المساعدة / Help

للحصول على مساعدة إضافية أو الإبلاغ عن مشكلة، يرجى التواصل مع مسؤول النظام.

---

For additional help or to report an issue, please contact your system administrator.