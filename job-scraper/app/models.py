from pydantic import BaseModel

class JobBase(BaseModel):
    title: str
    company: str
    location: str
    keyword: str

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: str