from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.analytics.models import DataSource, Event, DailyMetric, SavedReport

User = get_user_model()


class DataSourceModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            username="testuser",
            password="testpass123"
        )
        self.source = DataSource.objects.create(
            name="Web App",
            description="Frontend tracking",
            created_by=self.user
        )

    def test_create_datasource(self):
        self.assertEqual(self.source.name, "Web App")
        self.assertEqual(self.source.description, "Frontend tracking")
        self.assertEqual(self.source.created_by, self.user)

    def test_datasource_str(self):
        self.assertEqual(str(self.source), "Web App")

    def test_datasource_without_user(self):
        source = DataSource.objects.create(name="Anonymous Source")
        self.assertIsNone(source.created_by)


class EventModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            username="testuser",
            password="testpass123"
        )
        self.source = DataSource.objects.create(
            name="Mobile App",
            created_by=self.user
        )
        self.event = Event.objects.create(
            source=self.source,
            event_type="click",
            payload={"button": "submit", "page": "home"},
            user=self.user
        )

    def test_create_event(self):
        self.assertEqual(self.event.event_type, "click")
        self.assertEqual(self.event.payload["button"], "submit")
        self.assertEqual(self.event.source, self.source)
        self.assertEqual(self.event.user, self.user)

    def test_event_str(self):
        self.assertIn("click", str(self.event))

    def test_event_without_user(self):
        event = Event.objects.create(
            source=self.source,
            event_type="view",
            payload={"page": "landing"}
        )
        self.assertIsNone(event.user)


class DailyMetricModelTest(TestCase):

    def setUp(self):
        self.metric = DailyMetric.objects.create(
            date="2025-01-15",
            event_type="click",
            count=150,
            unique_users=45
        )

    def test_create_metric(self):
        self.assertEqual(self.metric.event_type, "click")
        self.assertEqual(self.metric.count, 150)
        self.assertEqual(self.metric.unique_users, 45)

    def test_metric_str(self):
        result = str(self.metric)
        self.assertIn("click", result)
        self.assertIn("150", result)


class SavedReportModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            username="testuser",
            password="testpass123"
        )
        self.report = SavedReport.objects.create(
            user=self.user,
            name="Reporte Semanal",
            config={
                "metric_type": "events_count",
                "dimensions": ["source"],
                "filters": {"date_range": "7d"}
            }
        )

    def test_create_report(self):
        self.assertEqual(self.report.name, "Reporte Semanal")
        self.assertEqual(self.report.user, self.user)
        self.assertEqual(self.report.config["metric_type"], "events_count")

    def test_report_str(self):
        self.assertEqual(str(self.report), "Reporte Semanal")
