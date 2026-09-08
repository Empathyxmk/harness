use paulocode_picostation::subq::*;

#[test]
fn test_subq_public() {
    // Assign test pointers (simulate the externs)
    IS_DATA_TRACK.with(|v| *v.borrow_mut() = vec![false, false]);
    LOGICAL_TRACK_TO_SECTOR.with(|v| *v.borrow_mut() = vec![0, 0]);
    // Public Test: sector == 0, num_logical_tracks > 2
    reset_globals(Some(5));
    SECTOR.with(|s| *s.borrow_mut() = 0);
    NUM_LOGICAL_TRACKS.with(|n| *n.borrow_mut() = 5);
    start_subq();
    HASDATA.with(|h| assert_eq!(*h.borrow(), 1));

    // Public Test: sector == 2 -> hasData = true
    reset_globals(None);
    SECTOR.with(|s| *s.borrow_mut() = 2);
    start_subq();
    HASDATA.with(|h| assert_eq!(*h.borrow(), 1));

    // Public Test: sector == 3 -> hasData = false
    reset_globals(None);
    SECTOR.with(|s| *s.borrow_mut() = 3);
    start_subq();
    HASDATA.with(|h| assert_eq!(*h.borrow(), 0));

    // Public Test: sector > 2, is_data_track[1] = true --> update
    reset_globals(None);
    SECTOR.with(|s| *s.borrow_mut() = 5);
    IS_DATA_TRACK.with(|id| if id.borrow().len() > 1 { id.borrow_mut()[1] = true; });
    LOGICAL_TRACK_TO_SECTOR.with(|lts| if lts.borrow().len() > 1 { lts.borrow_mut()[1] = 123; });
    start_subq();
    SECTOR_FOR_TRACK_UPDATE.with(|sf| assert_eq!(*sf.borrow(), 123));

    // Public Test: sector > 2, is_data_track[1] = false --> no update
    reset_globals(None);
    SECTOR.with(|s| *s.borrow_mut() = 8);
    IS_DATA_TRACK.with(|id| if id.borrow().len() > 1 { id.borrow_mut()[1] = false; });
    LOGICAL_TRACK_TO_SECTOR.with(|lts| if lts.borrow().len() > 1 { lts.borrow_mut()[1] = 77; });
    start_subq();
    SECTOR_FOR_TRACK_UPDATE.with(|sf| assert_eq!(*sf.borrow(), 0));

    // Public Test: printf_subq (smoke test with new data)
    let data: [u8;12] = [11,12,13,14,15,16,17,18,19,20,21,22];
    printf_subq(&data);
}