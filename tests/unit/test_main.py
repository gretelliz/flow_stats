"""Module to test the main napp file."""
from unittest import TestCase
from unittest.mock import patch

from napps.amlight.flow_stats.tests.helpers import get_controller_mock


# pylint: disable=too-many-public-methods, too-many-lines
class TestMain(TestCase):
    """Test the Main class."""

    def setUp(self):
        """Execute steps before each tests.

        Set the server_name_url_url from amlight/flow_stats
        """
        self.server_name_url = "http://localhost:8181/api/amlight/flow_stats"

        # The decorator run_on_thread is patched, so methods that listen
        # for events do not run on threads while tested.
        # Decorators have to be patched before the methods that are
        # decorated with them are imported.
        patch("kytos.core.helpers.run_on_thread", lambda x: x).start()
        # pylint: disable=import-outside-toplevel
        from napps.amlight.flow_stats.main import Main

        self.napp = Main(get_controller_mock())

    @staticmethod
    def get_napp_urls(napp):
        """Return the amlight/flow_stats urls.

        The urls will be like:

        urls = [
            (options, methods, url)
        ]

        """
        controller = napp.controller
        controller.api_server.register_napp_endpoints(napp)

        urls = []
        for rule in controller.api_server.app.url_map.iter_rules():
            options = {}
            for arg in rule.arguments:
                options[arg] = f"[{0}]".format(arg)

            if f"{napp.username}/{napp.name}" in str(rule):
                urls.append((options, rule.methods, f"{str(rule)}"))

        return urls

    def test_verify_api_urls(self):
        """Verify all APIs registered."""

        expected_urls = [
            (
                {"dpid": "[dpid]"},
                {"OPTIONS", "HEAD", "GET"},
                "/api/amlight/flow_stats/flow/match/ "
            ),
            (
                {"dpid": "[dpid]"},
                {"OPTIONS", "HEAD", "GET"},
                "/api/amlight/flow_stats/flow/stats/"
            ),
            (
                {"flow_id": "[flow_id]"},
                {"OPTIONS", "HEAD", "GET"},
                "/api/amlight/flow_stats/packet_count/"
            ),
            (
                {"flow_id": "[flow_id]"},
                {"OPTIONS", "HEAD", "GET"},
                "/api/amlight/flow_stats/bytes_count/"
            ),
            (
                {"dpid": "[dpid]"},
                {"OPTIONS", "HEAD", "GET"},
                "/api/amlight/flow_stats/packet_count/per_flow/"
            ),
            (
                {"dpid": "[dpid]"},
                {"OPTIONS", "HEAD", "GET"},
                "/api/amlight/flow_stats/packet_count/sum/"
            ),
            (
                {"dpid": "[dpid]"},
                {"OPTIONS", "HEAD", "GET"},
                "/api/amlight/flow_stats/bytes_count/per_flow/"
            ),
            (
                {"dpid": "[dpid]"},
                {"OPTIONS", "HEAD", "GET"},
                "/api/amlight/flow_stats/bytes_count/sum/"
            ),
        ]
        urls = self.get_napp_urls(self.napp)
        print(urls)
        self.assertEqual(len(expected_urls), len(urls))
