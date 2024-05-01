$(document).ready(function() {
    $('#competition').on('change', function() {
        var competition = $(this).val();
        $.ajax({
            url: '/get_teams',
            type: 'GET',
            data: { competition: competition },
            success: function(data) {
                var teamNames = data.split('\n');
                var team1Options = '<option value="" disabled selected>Select Team</option>';
                var team2Options = '<option value="" disabled selected>Select Team</option>';
                for (var i = 0; i < teamNames.length; i++) {
                    team1Options += '<option value="' + (i + 1) + '">' + teamNames[i] + '</option>';
                    team2Options += '<option value="' + (i + 1) + '">' + teamNames[i] + '</option>';
                }
                $('#team1').html(team1Options);
                $('#team2').html(team2Options);
            }
        });
    });

    $('#team1').on('change', function() {
        var selectedTeam = $(this).val();
        $('#team2 option[value="' + selectedTeam + '"]').attr('disabled', true);
    });

    $('#team2').on('change', function() {
        var selectedTeam = $(this).val();
        $('#team1 option[value="' + selectedTeam + '"]').attr('disabled', true);
    });
});