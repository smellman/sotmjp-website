from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from symposion.proposals.models import ProposalBase


@python_2_unicode_compatible
class ProposalCategory(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("proposal category")
        verbose_name_plural = _("proposal categories")


class Proposal(ProposalBase):

    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    AUDIENCE_LEVEL_INTERMEDIATE = 3

    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, _("Novice")),
        (AUDIENCE_LEVEL_INTERMEDIATE, _("Intermediate")),
        (AUDIENCE_LEVEL_EXPERIENCED, _("Experienced")),
    ]

    audience_level = models.IntegerField(
        choices=AUDIENCE_LEVELS,
        help_text=_('Level of audience expertise.'),
        verbose_name=_('Skill level'))
    recording_release = models.BooleanField(
        _("Recording Release"),
        default=True,
        help_text=_("By submitting your talk proposal, you agree to give "
                    "permission to the Organization Team to record, edit, "
                    "and release audio and/or video of your presentation. "
                    "If you do not agree to this, please uncheck this box.")
    )

    STATUS_UNREVIEWED = 1
    STATUS_ACCEPTED = 2
    STATUS_REJECTED = 3

    STATUS_OPTIONS = [
        (STATUS_UNREVIEWED, _('Not Yet Reviewed')),
        (STATUS_ACCEPTED, _('Accepted')),
        (STATUS_REJECTED, _('Rejected')),
    ]

    category = models.ForeignKey(ProposalCategory, verbose_name=_("Category"))
    overall_status = models.IntegerField(
        choices=STATUS_OPTIONS,
        default=STATUS_UNREVIEWED,
        help_text=_('The status of the proposal.'),
        verbose_name=_("Overall status"))

    REJECTION_POSTER = 1
    REJECTION_LIGHTNING = 2
    REJECTION_MOVED = 3
    REJECTION_DUPLICATE = 4
    REJECTION_ADMIN = 5
    REJECTION_BAD = 6

    REJECTION_OPTIONS = [
        (REJECTION_POSTER, _('Suggest re-submission as poster.')),
        (REJECTION_LIGHTNING, _('Suggest lightening talk.')),
        (REJECTION_MOVED, _('Re-submitted under appropriate category.')),
        (REJECTION_DUPLICATE, _('Duplicate')),
        (REJECTION_ADMIN, _('Administrative Action (Other)')),
        (REJECTION_BAD, _("No really: rejected. It's just plain bad.")),
    ]

    rejection_status = models.IntegerField(
        blank=True,
        null=True,
        choices=REJECTION_OPTIONS,
        help_text=_('The reason the proposal was rejected.'),
        verbose_name=_("Rejection status"))

    additional_requirements = models.TextField(
        _("Additional requirements"),
        blank=True,
        help_text=_("Please let us know if you have any specific needs"
                    "(A/V requirements, multiple microphones, a table, etc)."
                    "Note for example that 'audio out' is not provided"
                    "for your computer unless you tell us in advance.")
    )

    class Meta:
        abstract = True


class TalkProposal(Proposal):

    DURATION_CHOICES = [
        (0, _("No preference")),
        (1, _("10min")),
        (2, _("20min")),
    ]

    duration = models.IntegerField(choices=DURATION_CHOICES,
                                   verbose_name=_("Duration"))

    outline = models.TextField(
        _("Outline")
    )
    audience = models.CharField(
        max_length=150,
        verbose_name=_("Audience"),
        help_text=_('Who is the intended audience for your talk?'),
    )
    perceived_value = models.TextField(
        _("Objectives"),
        max_length=400,
        help_text=_("What will attendees get out of your talk?"),
    )

    class Meta:
        verbose_name = _("Talk proposal")
        verbose_name_plural = _("Talk proposals")


class LightningTalkProposal(Proposal):

    class Meta:
        verbose_name = _("Lightning talk proposal")
        verbose_name_plural = _("Lightning talk proposals")


class PosterProposal(Proposal):
    class Meta:
        verbose_name = _("Poster proposal")
        verbose_name_plural = _("Poster proposals")


class OpenSpaceProposal(Proposal):
    class Meta:
        verbose_name = _("Open Space proposal")
        verbose_name_plural = _("Open Space proposals")
