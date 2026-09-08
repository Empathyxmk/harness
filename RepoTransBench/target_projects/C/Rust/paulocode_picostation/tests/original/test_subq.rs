use paulocode_picostation::subq::*;

#[test]
fn test_subq_full() {
    reset_globals(None);
    // Test: sector == 0, num_logical_tracks > 1 --> hasData = true
    SECTOR.with(|s| *s.borrow_mut() = 0);
    NUM_LOGICAL_TRACKS.with(|n| *n.borrow_mut() = 2);
    start_subq();
    HASDATA.with(|h| assert_eq!(*h.borrow(), 1));

    // Test: sector == 1 -> hasData = false
    reset_globals(None);
    SECTOR.with(|s| *s.borrow_mut() = 1);
    start_subq();
    HASDATA.with(|h| assert_eq!(*h.borrow(), 0));

    // Test: sector == 2 -> hasData = true
    reset_globals(None);
    SECTOR.with(|s| *s.borrow_mut() = 2);
    start_subq();
    HASDATA.with(|h| assert_eq!(*h.borrow(), 1));

    // Test: sector > 2, is_data_track[1] = true --> update
    reset_globals(None);
    SECTOR.with(|s| *s.borrow_mut() = 3);
    IS_DATA_TRACK.with(|id| if id.borrow().len() > 1 { id.borrow_mut()[1] = true; });
    LOGICAL_TRACK_TO_SECTOR.with(|lts| if lts.borrow().len() > 1 { lts.borrow_mut()[1] = 199; });
    start_subq();
    SECTOR_FOR_TRACK_UPDATE.with(|sf| assert_eq!(*sf.borrow(), 199));

    // Test: sector > 2, is_data_track[1] = false --> no update
    reset_globals(None);
    SECTOR.with(|s| *s.borrow_mut() = 4);
    IS_DATA_TRACK.with(|id| if id.borrow().len() > 1 { id.borrow_mut()[1] = false; });
    LOGICAL_TRACK_TO_SECTOR.with(|lts| if lts.borrow().len() > 1 { lts.borrow_mut()[1] = 202; });
    start_subq();
    SECTOR_FOR_TRACK_UPDATE.with(|sf| assert_eq!(*sf.borrow(), 0));

    // Test printf_subq (smoke test)
    let data: [u8;12] = [0,1,2,3,4,5,6,7,8,9,10,11];
    printf_subq(&data);
}