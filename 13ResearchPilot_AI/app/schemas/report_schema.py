from pydantic import BaseModel, Field


class ResearchSource(BaseModel):
    title: str = Field(description="Title of the original research source")

    url: str = Field(description="Original URL of the research source")


class ResearchReport(BaseModel):
    topic: str = Field(description="Research topic")

    research_methodology: str = Field(
        description="Brief explanation of how the research was conducted using the provided sources"
    )

    executive_summary: str = Field(description="Brief overview of the research")

    key_findings: list[str] = Field(
        description="Important findings supported by the research sources"
    )

    important_insights: list[str] = Field(
        description="Important insights and observations derived from the collected research"
    )

    limitations: list[str] = Field(
        description="Research limitations, missing information, or areas requiring further investigation"
    )

    conclusion: str = Field(description="Overall conclusion based on the research")

    sources: list[ResearchSource] = Field(
        description="Original sources used in the research"
    )
