import logging

from django.conf import settings
from django.core.management import BaseCommand
from edx_rest_api_client.client import EdxRestApiClient

from course_discovery.apps.course_metadata.data_loaders import (
    CoursesApiDataLoader,
    DrupalApiDataLoader,
    OrganizationsApiDataLoader,
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Refresh course metadata from external sources.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--access_token',
            action='store',
            dest='access_token',
            default=None,
            help='OAuth2 access token used to authenticate API calls.'
        )

    def handle(self, *args, **options):
        access_token = options.get('access_token')

        if not access_token:
            logger.info('No access token provided. Retrieving access token using client_credential flow...')

            try:
                access_token, __ = EdxRestApiClient.get_oauth_access_token(
                    '{root}/access_token'.format(root=settings.SOCIAL_AUTH_EDX_OIDC_URL_ROOT),
                    settings.SOCIAL_AUTH_EDX_OIDC_KEY,
                    settings.SOCIAL_AUTH_EDX_OIDC_SECRET
                )
            except Exception:
                logger.exception('No access token provided or acquired through client_credential flow.')
                raise

        OrganizationsApiDataLoader(settings.ORGANIZATIONS_API_URL, access_token).ingest()
        CoursesApiDataLoader(settings.COURSES_API_URL, access_token).ingest()
        DrupalApiDataLoader(settings.MARKETING_API_URL).ingest()