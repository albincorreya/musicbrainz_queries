
import mbdata.models as models



def load_artist(session, artistGid):
    rec = session.query(models.Artist).filter_by(gid=artistGid).first()
    if rec is None:
        redir = session.query(models.ArtistGIDRedirect).filter_by(gid=artistGid).first()
        if redir is None:
            return None
        return redir.artist
    return rec


def load_releaseGroup(session, releaseGid):
    rec = session.query(models.ReleaseGroup).filter_by(gid=releaseGid).first()
    if rec is None:
        redir = session.query(models.ReleaseGroupGIDRedirect).filter_by(gid=releaseGid).first()
        if redir is None:
            return None
        return redir.releasegroup
    return rec



def load_recording(session, recordingGid):
    rec = session.query(models.Recording).filter_by(gid=recordingGid).first()
    if rec is None:
        redir = session.query(models.RecordingGIDRedirect).filter_by(gid=recordingGid).first()
        if redir is None:
            return None
        return redir.recording
    return rec



def load_work(session, workGid):
    rec = session.query(models.Work).filter_by(gid=workGid).first()
    if rec is None:
        redir = session.query(models.WorkGIDRedirect).filter_by(gid=workGid).first()
        if redir is None:
            return None
        return redir.work
    return rec
