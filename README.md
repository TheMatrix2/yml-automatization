# Modules for automatization of YML feeds generation

## Пример блока shop

    <shop version="2.0" date="2024-12-10 08:06">
      <name>Яндекс.Здоровье</name>
      <company>ООО Яндекс.Врачи</company>
      <url>https://example.ru/</url>
      <doctors>...</doctors>
      <clinics>...</clinics>
      <services>...</services>
      <offers>...</offers>
    </shop>

## Пример блока doctor

    <doctor id="doctor_1">
      <name>Иванов Иван Иванович</name>
      <url>https://example.ru/doctors/2246852315/</url>
      <description>Высококвалифицированный специалист - универсал со множеством специализаций!</description>
      <internal_id>2246852315</internal_id>
      <first_name>Иван</first_name>
      <surname>Иванов</surname>
      <patronymic>Иванович</patronymic>
      <experience_years>9</experience_years>
      <career_start_date>2015-01-01</career_start_date>
      <degree>доктор медицинских наук</degree>
      <rank>Профессор</rank>
      <category>Первая</category>
      <education>
        <organization>Медицинский университет Реавиз</organization>
        <finish_year>2010</finish_year>
        <type>Специалитет</type>
        <specialization>Лечебное дело (Лечебно-профилактическое дело)</specialization>
      </education>
      <job>
        <organization>Яндекс.Врачи</organization>
        <period_years>2010-н.в.</period_years>
        <position>Терапевт</position>
      </job>
      <certificate>
        <organization>Московский институт психоанализа</organization>
        <finish_year>2020</finish_year>
        <name>Лечебная физкультура и спортивная медицина</name>
      </certificate>
      <reviews_total_count>100</reviews_total_count>
      <review>
        <date>2024-12-07 09:00:24</date>
        <checked>true</checked>
        <used_in_rating>true</used_in_rating>
        <author>Наталья</author> 
        <author_id>natalia123</author_id>
        <author_picture>https://example.ru/reviews/natalia123.png</author_picture>
        <url>https://example.ru/doctors/2246852315/reviews</url>
        <comment>Долго ждать в регистратуре</comment>
        <grade>4.5</grade>
        <positive>Что-то, что понравилось</positive>
        <negative>Что-то, что не понравилось</negative>
        <response>Спасибо за отзыв!</response>
      </review>
    </doctor>

## Пример блока clinic

    <clinic id="clinic_1">
      <url>https://www.clinic.example.ru</url>
      <picture>https://www.clinic.example.ru/logo.jpg</picture>
      <name>Клиника Яндекс Здоровье</name>
      <city>г. Москва</city>
      <address>ул. Льва Толстого, 16</address>
      <email>info@example.ru</email>
      <phone>+79999999999</phone>
      <internal_id>123</internal_id>
      <company_id>1032739194</company_id>
    </clinic>

## Пример блока service

    <service id="service_1">
      <name>Первичный приём</name>
      <gov_id>A01.07.001</gov_id>
      <description>Первичный приём стоматолога-хирурга, диагностика возможности и степени хирургического вмешательства</description>
      <internal_id>123</internal_id>
    </service>

