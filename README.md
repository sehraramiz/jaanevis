Some related notes on some related locations around the world

این پروژه از طراحی و توضیحات [این کتاب](https://leanpub.com/clean-architectures-in-python) برای تست و تمرین معماری تمیز الگو گرفته.

همه‌ی اجزا مبتنی بر کتاب اصلی معماری تمیز نیست یه سری چیزها کم و زیاد هست. ولی اصولا [اجزای مهم معماری تمیز](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) مثلا رعایت مرزبندی‌ها رو سعی میکنم به هم نزنم.

برای پروژه‌هایی که صرفا یه سری سرویس crud و احراز هویت هستند (مثل این پروژه) استفاده از این معماری یا مشابهش توجیحی نداره. صرفا روند توسعه رو کندتر میکنه.

اهداف کلی:

۱- مستقل از فریمورک

۲- قابلیت تست پذیری مستقل از دیتابیس، ui، وب‌سرور

۳- مستقل از نوع دیتابیس

![Clean Architecture Diagram](./pic/CleanArchitecture.jpg)

- ماژول `usecases` - محل بیزینس لاجیک - همون لایه‌ی Use Cases هست
- ماژول `domain` همون Entities
- ماژول `repository` لابه‌ی Presenters
- ماژول `api` شامل cli و fastapi و همچنین بقیه‌ی ابزارها مثل ابزار ارسال ایمیل یا دیتابیس معادل لایه‌ی آخر

در لایه‌ی داخلی نمیشه به لایه‌ی بالایی دسترسی داشت مگر با رابط

مثلا در لایه‌ی usecases نمیشه به لایه‌ی بالاتر دسترسی مستقیم داشت. فقط از طریق یک نوع رابط مثل repository امکانش هست.

مصداق دسترسی مستقیم میشه همون ایمپورت مستقیم

در ادامه چنتا مسئله پیش میاد
- وقتی مدل دیتابیس مثل مدل orm جنگو یا sqlalchemy داشته باشیم جایگاه این مدل کجا باید باشه که خلاف محدودیت‌های تعریف شده نباشه
- آیا با عوض شدن کاربری مدل دیتابیس برای رعایت خط قرمزای معماری، امکانات خوبی که orm در اختیارمون میذاره حیف و میل میشه؟
- آیا بقیه امکانات جنگو هم حیف و میل میشه؟ مثلا استفاده از احراز هویت خود جنگو با محدودیتای تعریف شده تناقض داره؟


### translations

0- install [gnu gettext](https://www.gnu.org/software/gettext/) to access msgfmt, xgettext,  msgmerge tools


1- create/update language .po file
```bash
make LANG=fa makemessages
```

2- translate messages in ```jaanevis/i18n/locales/fa/LC_MESSAGES/messages.po```

3- compile translation to .mo file
```bash
make LANG=fa compilemessages
```
